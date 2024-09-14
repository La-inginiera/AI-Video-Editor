import json
from moviepy.editor import VideoFileClip
import logging
logging.basicConfig(level=logging.ERROR)


from .tool_actions import (
    add_text_overlay, blur_region_of_frame, remove_frames, apply_grayscale_filter,
    add_voiceover, crop_video, change_speed, add_background_music, stabilize_video,
    adjust_brightness_contrast, add_watermark, track_object, detect_scenes,
    apply_transitions, apply_chroma_key, apply_cartoon_effect, morph_faces,
    super_resolution_enhancement, detect_pose
)

def execute_tool_suggestions(frame, tools):
    """
    This function takes in a frame and an array of tool suggestions (functions with their arguments)
    and applies each function to the frame.

    Args:
        frame (ndarray): The current video frame to process.
        tools (list): A list of tool function calls in the format:
                      "{ functions: [{ 'name': 'function_name', 'arguments': '{ ... }' }] }"

    Returns:
        frame: The processed video frame after applying all tool suggestions.
    """
    # Loop through each tool call in the list of tools
    for tool_call in tools['functions']:
        tool_name = tool_call['name']
        arguments = tool_call['arguments']        

        try:
            # Apply each tool based on the tool_name
            if tool_name == "add_text_overlay":
                text = arguments.get('text', 'Default Text')
                position = arguments.get('position', 'bottom')
                frame = add_text_overlay(frame, text, position)

            elif tool_name == "blur_region":
                region = arguments.get('region', [0, 0, 100, 100])  # Default region if not provided
                frame = blur_region_of_frame(frame, region)

            elif tool_name == "apply_grayscale_filter":
                frame = apply_grayscale_filter(frame)

            elif tool_name == "adjust_brightness_contrast":
                brightness = arguments.get('brightness', 30)  # Default to 30 if not provided
                contrast = arguments.get('contrast', 30)      # Default to 30 if not provided
                frame = adjust_brightness_contrast(frame, brightness, contrast)

            elif tool_name == "apply_cartoon_effect":
                frame = apply_cartoon_effect(frame)

            elif tool_name == "apply_chroma_key":
                background_image = arguments.get('background_image', 'default_background.jpg')  # Default background
                lower_green = arguments.get('lower_green', [35, 43, 46])
                upper_green = arguments.get('upper_green', [77, 255, 255])
                frame = apply_chroma_key(frame, background_image, lower_green, upper_green)

            elif tool_name == "detect_pose":
                frame = detect_pose(frame)

            elif tool_name == "super_resolution_enhancement":
                frame = super_resolution_enhancement(frame)

            elif tool_name == "add_voiceover":
                text = arguments.get('text', 'Sample voiceover text')
                frame = add_voiceover(frame, text)

            elif tool_name == "crop_video":
                x1 = arguments['x1']
                y1 = arguments['y1']
                x2 = arguments['x2']
                y2 = arguments['y2']
                frame = crop_video(frame, x1, y1, x2, y2)

            elif tool_name == "change_speed":
                factor = arguments.get('factor', 1.0)
                frame = change_speed(frame, factor)

            elif tool_name == "add_background_music":
                music_file = arguments.get('music_file', 'background.mp3')
                frame = add_background_music(frame, music_file)

            elif tool_name == "stabilize_video":
                input_path = arguments['input_path']
                output_path = arguments['output_path']
                stabilize_video(input_path, output_path)

            elif tool_name == "add_watermark":
                watermark_image = arguments['watermark_image']
                position = arguments.get('position', 'bottom-right')
                frame = add_watermark(frame, watermark_image, position)

            elif tool_name == "track_object":
                tracker_type = arguments.get('tracker_type', 'CSRT')
                region = arguments.get('region', [50, 50, 100, 100])
                track_object('input_video.mp4', 'output_tracked.mp4', tracker_type)

            elif tool_name == "scene_detection_transition_effects":
                scenes = detect_scenes('input_video.mp4')
                transition_type = arguments.get('transition_type', 'fade')
                frame = apply_transitions(frame, scenes, transition_type)

            elif tool_name == "morph_faces":
                face1 = arguments['face1']
                face2 = arguments['face2']
                alpha = arguments.get('alpha', 0.5)
                frame = morph_faces(face1, face2, alpha)
        
        except Exception as e:
            logging.info(f"An error occurred while processing tool action: {e}")

    return frame
