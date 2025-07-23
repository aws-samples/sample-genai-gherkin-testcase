import json
import os
import sys
from ipywidgets import Dropdown
from common.common import read_api_specification, get_response_code_for_method, get_methods, get_paths, split

from prompts.gherkin_prompt_placeholder import gherkin_prompt_placeholder

# Define Models parameter
temperature = 0

top_k = 250
top_p = 1

# Base inference parameters.
inference_config = {
    "temperature": temperature,
    "topP": top_p
}
# Additional model inference parameters.
additional_model_fields = {"top_k": top_k}

if not os.path.exists("input"):
    os.makedirs("input")

input_options = ["-"] + os.listdir("input")
input_api_spec_file_dropdown = Dropdown(options=input_options)
input_api_spec_path_dropdown = Dropdown(options=["-"])
input_api_spec_method_dropdown = Dropdown(options=["-"])
input_api_spec_response_code_dropdown = Dropdown(options=["-"])


def refresh_input():
    input_folders = ["-"] + os.listdir("input")
    input_api_spec_file_dropdown.options = input_folders


def read_api_spec(filepath):
    try:
        return read_api_specification(filepath)
    except Exception as e:
        pass


def change_method_dropdown(change):
    filepath = "./input/" + input_api_spec_file_dropdown.value
    path = input_api_spec_path_dropdown.value
    method = change.new
    try:
        spec = read_api_spec(filepath)
        input_api_spec_response_code_dropdown.options = get_response_code_for_method(spec, path, method)
    except Exception as e:
        input_api_spec_response_code_dropdown.options = ["-"]


def change_path_dropdown(change):
    filepath = "./input/" + input_api_spec_file_dropdown.value
    path = change.new
    try:
        spec = read_api_spec(filepath)
        input_api_spec_method_dropdown.options = get_methods(spec, path)
    except Exception as e:
        input_api_spec_method_dropdown.options = ["-"]


def change_input_file_dropdown(change):
    filepath = "./input/" + change.new
    try:
        spec = read_api_spec(filepath)
        input_api_spec_path_dropdown.options = get_paths(read_api_spec(filepath))
    except Exception as e:
        input_api_spec_path_dropdown.options = ["-"]

input_api_spec_file_dropdown.observe(change_input_file_dropdown, 'value')
input_api_spec_path_dropdown.observe(change_path_dropdown, 'value')
input_api_spec_method_dropdown.observe(change_method_dropdown, 'value')

def get_gherkin_prompt_message():
    input_file_path = "./input/" + input_api_spec_file_dropdown.value
    api_spec_file_name = input_api_spec_file_dropdown.value
    path = input_api_spec_path_dropdown.value
    operation = input_api_spec_method_dropdown.value
    response_code = input_api_spec_response_code_dropdown.value

    if input_file_path == "./input/-" or path == "-" or operation == "-" or response_code == "-":
        print("Choose appropriate values")
        sys.exit(1)

    try:
        input_spec_content = read_api_specification(input_file_path)
    except Exception as e:
        print(f"Error reading API specification: {e}")
        sys.exit(1)
    api_spec = split(input_spec_content, path, operation)

    input_length = len(json.dumps(input_spec_content))
    trimmed_length = len(json.dumps(api_spec))
    saving = input_length - trimmed_length
    percentage_saving = int((saving / input_length) * 100)

    print("Original Size: {}, trimmed size: {}, Percentage Saving: {}".format(input_length, trimmed_length,
                                                                              percentage_saving))

    print(f'{path}')
    print(operation)
    print(response_code)
    user_message = gherkin_prompt_placeholder.format(spec=api_spec, API_PATH=f'{path}', HTTP_OPERATION=operation,
                                                         HTTP_RESPONSE_CODE=response_code)

    message = {
        "role": "user",
        "content": [
            {
                "text": user_message,
            },
            {
                "cachePoint": {
                    "type": "default"
                }
            }
        ]
    }
    return api_spec_file_name, path, operation, response_code, [message]
