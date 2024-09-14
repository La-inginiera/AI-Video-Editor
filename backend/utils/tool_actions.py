import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from gtts import gTTS
from vidstab import VidStab
from moviepy.video.fx.speedx import speedx
import mediapipe as mp
from scenedetect import SceneManager, open_video, ContentDetector

# Helper function to resize frames to maintain uniformity
def ensure_frame_size(frame, target_size):
    return cv2.resize(frame, target_size)

# Add text overlay to a video clip using Pillow (PIL)
from PIL import ImageFont, ImageDraw

def add_text_overlay(video_clip, text, position="bottom"):
    def process_frame(frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # Use a common font like Arial with size 24
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # This assumes 'arial.ttf' is available on your system
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if arial isn't found

        # Draw text
        draw = ImageDraw.Draw(pil_img)

        # Calculate text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[1] - text_bbox[0]
        text_height = text_bbox[2] - text_bbox[0]

        # Set text position
        if position == "bottom":
            text_position = ((frame.shape[1] - text_width) // 2, frame.shape[0] - text_height - 10)
        elif position == "top":
            text_position = ((frame.shape[1] - text_width) // 2, 10)
        else:
            text_position = ((frame.shape[1] - text_width) // 2, (frame.shape[0] - text_height) // 2)

        # Draw the text on the image
        draw.text(text_position, text, font=font, fill="white")

        # Convert back to BGR for OpenCV
        frame_with_text = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return frame_with_text

    return video_clip.fl_image(process_frame)


# Blur a specific region of a video clip
def blur_region_of_frame(video_clip, region):
    def process_frame(frame):
        (x, y, w, h) = region
        sub_frame = frame[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(sub_frame, (21, 21), 30)
        frame[y:y+h, x:x+w] = blurred
        return frame

    return video_clip.fl_image(process_frame)

# Apply grayscale filter to a video clip
def apply_grayscale_filter(video_clip):
    def process_frame(frame):
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(grayscale_frame, cv2.COLOR_GRAY2BGR)

    return video_clip.fl_image(process_frame)

# Add voiceover to a video clip
def add_voiceover(video_clip, text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save("voiceover.mp3")
    audio_clip = AudioFileClip("voiceover.mp3")
    return video_clip.set_audio(audio_clip)

# Adjust brightness and contrast of a video clip
def adjust_brightness_contrast(video_clip, brightness=30, contrast=30):
    def process_frame(frame):
        return cv2.convertScaleAbs(frame, alpha=1 + contrast / 127.0, beta=brightness)

    return video_clip.fl_image(process_frame)

# Add watermark to a video clip
def add_watermark(video_clip, watermark_image, position="bottom-right"):
    def process_frame(frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        watermark = Image.open(watermark_image).resize((50, 50))
        if position == "bottom-right":
            pos = (frame.shape[1] - watermark.width - 10, frame.shape[0] - watermark.height - 10)
        pil_img.paste(watermark, pos, watermark)

        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    return video_clip.fl_image(process_frame)

# Apply a cartoon effect to a video clip
def apply_cartoon_effect(video_clip):
    def process_frame(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    return video_clip.fl_image(process_frame)

# Chroma keying (Green screen removal) in a video clip
def apply_chroma_key(video_clip, background_image, lower_green, upper_green):
    def process_frame(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.imread(background_image)
        bg = cv2.resize(bg, (frame.shape[1], frame.shape[0]))

        fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        bg = cv2.bitwise_and(bg, bg, mask=mask)
        return cv2.add(fg, bg)

    return video_clip.fl_image(process_frame)

# Crop a video clip
def crop_video(video_clip, x1, y1, x2, y2):
    return video_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

# Change the speed of a video clip
def change_speed(video_clip, factor):
    return video_clip.fx(speedx, factor)

# Add background music to a video clip
def add_background_music(video_clip, music_file):
    music = AudioFileClip(music_file).subclip(0, video_clip.duration)
    return video_clip.set_audio(music)

# Stabilize a video
def stabilize_video(input_path, output_path):
    stabilizer = VidStab()
    stabilizer.stabilize(input_path=input_path, output_path=output_path)

# Remove specific frames from a video clip
def remove_frames(video_clip, start_time, end_time):
    clip_before = video_clip.subclip(0, start_time)
    clip_after = video_clip.subclip(end_time, video_clip.duration)
    return concatenate_videoclips([clip_before, clip_after])

# Track an object across video frames
def track_object(video_path, output_path, tracker_type="CSRT"):
    tracker = cv2.TrackerCSRT_create()
    video = cv2.VideoCapture(video_path)

    success, frame = video.read()
    bbox = cv2.selectROI("Select Object to Track", frame, False)
    tracker.init(frame, bbox)

    while True:
        success, frame = video.read()
        if not success:
            break
        success, bbox = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    video.release()
    cv2.destroyAllWindows()

# Detect scenes in the video
def detect_scenes(video_path):
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    video = open_video(video_path)
    scene_manager.detect_scenes(video)
    return scene_manager.get_scene_list()

# Apply transitions between scenes in a video clip
def apply_transitions(video_clip, scenes, transition_type="fade"):
    for scene in scenes:
        if transition_type == "fade":
            video_clip = video_clip.fadein(1).fadeout(1)
    return video_clip

# Morph faces between two frames
def morph_faces(face1, face2, alpha=0.5):
    return cv2.addWeighted(face1, alpha, face2, 1 - alpha, 0)

# Apply AI-based super-resolution enhancement to a video clip
def super_resolution_enhancement(video_clip):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel("ESPCN_x4.pb")
    sr.setModel("espcn", 4)
    return video_clip.fl_image(sr.upsample)

# Detect body pose in a video clip
def detect_pose(video_clip):
    def process_frame(frame):
        mp_pose = mp.solutions.pose.Pose()
        results = mp_pose.process(frame)
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        return frame

    return video_clip.fl_image(process_frame)
