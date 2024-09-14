from flask import Flask, request, jsonify, Response
from utils.gpt_interaction import get_gpt_tool_suggestions
from utils.processor import execute_tool_suggestions
from flask_cors import CORS
import threading
import cv2
import base64
import os
import json
import time
import numpy as np
from moviepy.editor import ImageSequenceClip

app = Flask(__name__)
CORS(app)

processing_status = {"progress": 0, "video": None}
processed_video_path = None

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    prompt = request.form.get('prompt')

    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    video_path = os.path.join(upload_folder, 'video.mp4')
    video.save(video_path)

    # Process video in background
    thread = threading.Thread(target=process_video, args=(video_path, prompt))
    thread.start()

    return jsonify({'status': 'upload_successful', 'message': 'Video is being processed.'}), 200

def process_video(video_path, prompt):
    global processing_status, processed_video_path
    processing_status["progress"] = 0

    # Capture video and process in chunks
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    processed_frames = []
    chunk_size = 20  # Process 20 frames at a time
    base64_frames_chunk = []
    video_chunk = []
    frame_number = 0
    progress_step = 100 / frame_count  # Progress per frame, not per chunk

    # Get the dimensions of the first frame to ensure consistency
    success, first_frame = video.read()
    if not success:
        return

    first_frame_height, first_frame_width = first_frame.shape[:2]
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to the first frame

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # Resize frame to match the dimensions of the first frame
        frame = cv2.resize(frame, (first_frame_width, first_frame_height))

        # Ensure the frame is in RGB format for MoviePy
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert frame to base64 for GPT-4 interaction
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(buffer).decode('utf-8')
        base64_frames_chunk.append(base64_frame)
        video_chunk.append(frame_rgb)  # Add RGB frame for MoviePy processing

        # Process each chunk of frames
        if len(base64_frames_chunk) == chunk_size or frame_number == frame_count - 1:
            # Send the base64 images to GPT-4 and get tool suggestions
            tools_responses = get_gpt_tool_suggestions(base64_frames_chunk, prompt)

            # Convert numpy frames (video_chunk) to VideoFileClip
            clip = ImageSequenceClip(video_chunk, fps=fps)

            # Now process the video chunk using the tool responses
            processed_clip = execute_tool_suggestions(clip, tools_responses)

            # Extract processed frames from the clip
            processed_chunk = list(processed_clip.iter_frames())

            # Resize the processed frames back to the first frame's dimensions (if needed)
            processed_chunk = [cv2.resize(frame, (first_frame_width, first_frame_height)) for frame in processed_chunk]

            # Append the processed frames to the final processed frames
            processed_frames.extend(processed_chunk)

            # Reset for the next chunk
            base64_frames_chunk = []
            video_chunk = []

        # Update the progress after every frame, not just after every chunk
        frame_number += 1
        processing_status["progress"] = round((frame_number / frame_count) * 100)

    video.release()

    # Save the processed video
    processed_video_path = 'uploads/processed_video.mp4'
    save_processed_video(processed_frames, processed_video_path, fps)

    # Once video is saved, prepare the base64 encoded video to be sent to the frontend
    with open(processed_video_path, 'rb') as f:
        video_data = base64.b64encode(f.read()).decode('utf-8')
        processing_status["video"] = f"data:video/mp4;base64,{video_data}"

    processing_status["progress"] = 100  # Mark processing as complete


def save_processed_video(frames, output_path, fps):
    """
    Ensure uniform size of frames using MoviePy for saving.
    """
    # Ensure all frames have the same dimensions as the first frame
    height, width, layers = frames[0].shape

    # Resize all frames to ensure uniformity
    resized_frames = [cv2.resize(frame, (width, height)) for frame in frames]

    # Save the processed frames using MoviePy
    clip = ImageSequenceClip([cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in resized_frames], fps=fps)
    clip.write_videofile(output_path, codec='libx264', audio=False)





@app.route('/status')
def status():
    def generate_status():
        while processing_status["progress"] < 100:
            yield f"data: {json.dumps({'progress': processing_status['progress']})}\n\n"
            time.sleep(3)  # Add a delay of 3 seconds between each progress update
        # When processing completes, stream the final status with the processed video
        if processing_status["video"]:
            yield f"data: {json.dumps({'progress': 100, 'video': processing_status['video']})}\n\n"

    return Response(generate_status(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True)
