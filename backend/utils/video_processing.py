import cv2
from moviepy.editor import VideoFileClip
import base64
import os

def extract_frames(video_path, seconds_per_frame=1):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * seconds_per_frame)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    base64_frames = []
    
    for frame_idx in range(0, total_frames, frame_interval):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frames.append(base64.b64encode(buffer).decode('utf-8'))
    
    video.release()
    
    # Extract audio
    audio_path = os.path.splitext(video_path)[0] + ".mp3"
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.audio.close()
    clip.close()
    
    return base64_frames, audio_path
