import json

def get_fixed_tool_calls_or_text_output(json_str, max_depth=5):
    text_output = try_fix_json(json_str, max_depth)
    if text_output[1] is True:
        parsed_text_out = text_output[0]
        return json.loads(parsed_text_out), "api_tool_calls"
    else:
        parsed_text_out = text_output[0].split("null-jianguo", 1)[0].strip()
        return parsed_text_out, "api_text_output"