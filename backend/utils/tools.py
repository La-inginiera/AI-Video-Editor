def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "add_text_overlay",
                "description": "Add custom text overlays to the video, such as subtitles, captions, or any user-specified text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The text to overlay on the video"},
                        "position": {"type": "string", "description": "The position of the text on the video", "enum": ["top", "bottom", "center"]},
                    },
                    "required": ["text"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "blur_region",
                "description": "Blur specific regions of the video, such as faces or license plates, for privacy or artistic effect.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "region": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "minItems": 4,
                            "maxItems": 4,
                            "description": "The region to blur in the format [x, y, width, height]"
                        }
                    },
                    "required": ["region"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "remove_frames",
                "description": "Remove specific frames from the video based on user input or model suggestions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_time": {"type": "integer", "description": "The start time of the frames to remove"},
                        "end_time": {"type": "integer", "description": "The end time of the frames to remove"},
                    },
                    "required": ["start_time", "end_time"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "apply_grayscale_filter",
                "description": "Convert the video to grayscale for a dramatic, classic look.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_voiceover",
                "description": "Add a custom voiceover to the video using text-to-speech.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The voiceover text"}
                    },
                    "required": ["text"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "crop_video",
                "description": "Crop the video to a specified region, trimming the edges and keeping only the relevant parts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x1": {"type": "integer", "description": "The x-coordinate of the top-left corner of the crop area"},
                        "y1": {"type": "integer", "description": "The y-coordinate of the top-left corner of the crop area"},
                        "x2": {"type": "integer", "description": "The x-coordinate of the bottom-right corner of the crop area"},
                        "y2": {"type": "integer", "description": "The y-coordinate of the bottom-right corner of the crop area"}
                    },
                    "required": ["x1", "y1", "x2", "y2"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "change_speed",
                "description": "Speed up or slow down the video based on user input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "factor": {"type": "number", "description": "The factor by which to speed up or slow down the video"}
                    },
                    "required": ["factor"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_background_music",
                "description": "Overlay background music onto the video, mixing it with the original audio or replacing it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "music_file": {"type": "string", "description": "The file path to the background music"}
                    },
                    "required": ["music_file"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "stabilize_video",
                "description": "Stabilize shaky video footage, making it smoother to watch.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_path": {"type": "string", "description": "The path to the input video file"},
                        "output_path": {"type": "string", "description": "The path to save the stabilized video"}
                    },
                    "required": ["input_path", "output_path"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "adjust_brightness_contrast",
                "description": "Adjust the brightness, contrast, or saturation of the video.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "brightness": {"type": "integer", "description": "The brightness level to apply to the video"},
                        "contrast": {"type": "integer", "description": "The contrast level to apply to the video"}
                    },
                    "required": ["brightness", "contrast"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_watermark",
                "description": "Insert a watermark (e.g., logo or text) to the video in a specified position.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watermark_image": {"type": "string", "description": "The file path to the watermark image"},
                        "position": {"type": "string", "description": "The position of the watermark on the video", "enum": ["top-left", "top-right", "bottom-left", "bottom-right"]}
                    },
                    "required": ["watermark_image"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "track_object",
                "description": "Track objects or people throughout the video and apply effects to the tracked object.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tracker_type": {"type": "string", "description": "The type of object tracker to use", "enum": ["KCF", "CSRT", "MOSSE"]},
                        "region": {"type": "array", "items": {"type": "integer"}, "minItems": 4, "maxItems": 4, "description": "The initial bounding box [x, y, width, height] for the object to track"}
                    },
                    "required": ["tracker_type", "region"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "scene_detection_transition_effects",
                "description": "Automatically detect different scenes in the video and apply custom transition effects between them.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transition_type": {"type": "string", "description": "The type of transition to apply between scenes", "enum": ["fade", "cut"]}
                    },
                    "required": ["transition_type"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "apply_chroma_key",
                "description": "Remove a green screen (or any background color) and replace it with a custom background or image.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "background_image": {"type": "string", "description": "The file path to the background image"},
                        "lower_green": {"type": "array", "items": {"type": "integer"}, "minItems": 3, "maxItems": 3, "description": "Lower bound for the green color in HSV format"},
                        "upper_green": {"type": "array", "items": {"type": "integer"}, "minItems": 3, "maxItems": 3, "description": "Upper bound for the green color in HSV format"}
                    },
                    "required": ["background_image", "lower_green", "upper_green"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "apply_cartoon_effect",
                "description": "Apply a cartoon-like effect to the video, making it look like an animated film.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "face_morphing",
                "description": "Morph faces between two individuals over time or swap faces in the same video.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "face1": {"type": "string", "description": "The file path to the first face image"},
                        "face2": {"type": "string", "description": "The file path to the second face image"},
                        "alpha": {"type": "number", "description": "The blending factor between the two faces"}
                    },
                    "required": ["face1", "face2"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "super_resolution_enhancement",
                "description": "Enhance the video resolution using AI-based super-resolution techniques.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resolution_factor": {"type": "number", "description": "The factor by which to enhance the resolution"}
                    },
                    "required": ["resolution_factor"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "detect_pose",
                "description": "Detect and track human body poses in the video, overlaying visual cues on top of the video to indicate the detected pose.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        }
    ]
