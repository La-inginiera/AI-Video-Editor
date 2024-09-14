from openai import OpenAI
import json
from config import config
from .tools import get_tools
from .general import remove_code_block_syntax

client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_gpt_tool_suggestions(frames, prompt):

    # return  { "functions": [{
    #   "name": "add_text_overlay",
    #   "arguments": {
    #     "text": "City view behind the park",
    #     "position": "bottom"
    #   } }]
    # }
    # Construct the frame data, for example using all 5 frames in the chunk
    frame_data = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpg;base64,{frame}"  # Base64-encoded frames
            }
        }
        for frame in frames
    ]
    
    # Build a detailed and descriptive prompt message
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "I have a video with multiple frames provided below. "
                        "The user has uploaded this video and requested specific edits based on the following prompt: "
                        f"'{prompt}'. "
                        "Your task is to analyze the provided frames and suggest appropriate video editing tools and techniques "
                        "to perform the requested modifications. "
                        "The available tools include: "
                        f"{get_tools()}.  "
                        "For each frame, generate a detailed suggestion in the format specified below detailing what editing tools should be applied. "
                        "Please provide the tool name, necessary parameters (like text, position, start/end times, region coordinates, etc.), "
                        "and ensure that the output format adheres **STRICTLY** to this schema below."
                        "Return only the JSON object. DO NOT INCLUDE ```json" 
                        "{ functions: [{ 'name': 'function name to call. Example: "
                        "'stabilize_video'', 'arguments': '{ 'a dictionary of arguments to pass to function' } }] }"
                    ),
                },
                *frame_data
            ]
        }
    ]

    # Call GPT-4 model with the detailed prompt
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500
    )

    # Extract tool suggestions from the response
    tools_response = response.choices[0].message.content
    print(tools_response)
    formatted_response = remove_code_block_syntax(tools_response)
    return json.loads(formatted_response)
