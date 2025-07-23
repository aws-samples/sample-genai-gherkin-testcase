from ipywidgets import *
from common.common import *
from prompts.gherkin_java_stub_prompt import gherkin_java_stub_prompt

if not os.path.exists("output/features"):
    os.makedirs("output/features")
if not os.path.exists("output/stubs"):
    os.makedirs("output/stubs")

options = ["-"] + os.listdir("output/features")

input_feature_dropdown = Dropdown(options=options)


def change_input_feature_dropdown(change):
    print(change)


def refresh_features():
    options = ["-"] + os.listdir("output/features")
    input_feature_dropdown.options = options


input_feature_dropdown.observe(change_input_feature_dropdown, 'value')


def get_java_stub_prompt_message():
    input_feature_file = input_feature_dropdown.value
    file_name = input_feature_dropdown.value.split(".feature")[0]
    with open("output/features/" + input_feature_file, 'r', encoding='utf-8') as file:
        input_feature_file_content = file.read()

    system_prompts = []
    user_message = gherkin_java_stub_prompt.format(feature_file=input_feature_file_content)

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
    return file_name, [message]
