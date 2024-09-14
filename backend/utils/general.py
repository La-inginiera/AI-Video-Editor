def remove_code_block_syntax(input_string):
    # Check if input starts with ```json and remove it
    if input_string.startswith("```json"):
        input_string = input_string[len("```json"):].strip()

    # Check if input ends with ``` and remove it
    if input_string.endswith("```"):
        input_string = input_string[:-len("```")].strip()

    return input_string