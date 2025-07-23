# Read the api spec provided in the input path. First try to load as yaml, then as Json.
# If we cannot load the content of the file exit.
# else return the api spec in json format.
import json
import yaml
from typing import Optional
import re
from pathlib import Path
from typing import Union

def read_api_specification(input_content):
    try:
        with open(input_content, 'r', encoding='utf-8') as file:
            content = file.read()
        # First try parsing as JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON fails, try YAML
            try:
                return yaml.safe_load(content)
            except yaml.YAMLError:
                raise ValueError("Invalid file format: File must be valid JSON or YAML")

    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {input_content}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {str(e)}")


# This function takes an input specification and trims down the spec for the specific path and the method.
# Returns the trimmed spec
def split(spec, path, method):
    result = {}
    try:
        for key in spec.keys():
            if key == "paths":
                result["paths"] = {}
                result["paths"][path] = {}
                for key in spec['paths'][path]:
                    if key.lower() in ["get", "post", "patch", "delete", "put", "options"]:
                        result["paths"][path][method] = spec['paths'][path][method]
                    else:
                        result["paths"][path][key] = spec['paths'][path][key]
            elif key == "components":
                result["components"] = spec[key]
            elif key == "definitions":
                result["definitions"] = spec[key]
            else:
                result[key] = spec[key]
    except KeyError:
        print("path or method not found")

    return result





def save_files(content: str, root: Union[str, Path], file_name: str) -> Path:
    """
    Save content to a file in the specified directory.

    Args:
        content (str): The content to write to the file
        root (Union[str, Path]): The directory path where the file should be saved
        file_name (str): The name of the file to create

    Returns:
        Path: The path to the saved file

    Raises:
        OSError: If there's an error creating the directory or writing the file
        TypeError: If the input types are incorrect
    """
    try:
        root_path = Path(root)
        root_path.mkdir(parents=True, exist_ok=True)
        # Create full file path
        file_path = root_path / file_name
        # Write content to file
        file_path.write_text(content, encoding='utf-8')
        return file_path

    except TypeError as e:
        raise TypeError(f"Invalid input types: {str(e)}")
    except OSError as e:
        raise OSError(f"Error saving file {file_name}: {str(e)}")


def parser(content: str, tag: str) -> Optional[str]:
    """
    Extract content between XML-style tags.

    Args:
        content (str): The string containing XML-style tags
        tag (str): The tag name to search for

    Returns:
        Optional[str]: The content between the tags, or None if tags not found

    """
    try:
        # Using regex for more robust parsing
        pattern = f"<{tag}>(.+?)</{tag}>"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            return match.group(1)
        return None

    except (TypeError, re.error) as e:
        raise ValueError(f"Error parsing content with tag '{tag}': {str(e)}")


def get_spec(spec, path, operation):
    return split(spec, path, operation)


def get_paths(json_spec_data):
    return [path for path in json_spec_data["paths"]]


def get_methods(json_spec_data, path):
    return [method for method in json_spec_data["paths"][path]]


def get_response_code_for_method(json_spec_data, path, method):
    try:
        return list(json_spec_data["paths"][path][method]["responses"])
    except KeyError as e:
        return []

# Stream conversation
def stream_conversation(bedrock_client,
                        model_id,
                        messages,
                        system_prompts,
                        inference_config,
                        additional_model_fields):
    """
    Sends messages to a model and streams the response.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send.
        system_prompts (JSON) : The system prompts to send.
        inference_config (JSON) : The inference configuration to use.
        additional_model_fields (JSON) : Additional model fields to use.

    Returns:
        Nothing.

    """

    response = bedrock_client.converse_stream(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields

    )

    stream = response.get('stream')
    result = ""
    if stream:
        for event in stream:

            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}")
                result = result + f"\nRole: {event['messageStart']['role']}" + "\n"
            if 'contentBlockDelta' in event:
                print(event['contentBlockDelta']['delta']['text'], end="")
                result = result + event['contentBlockDelta']['delta']['text'] + ""
            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}")
                result = result + f"\nStop reason: {event['messageStop']['stopReason']}"

            if 'metadata' in event:
                metadata = event['metadata']
                if 'usage' in metadata:
                    print("\nToken usage")
                    print(f"Input tokens: {metadata['usage']['inputTokens']}")
                    print(f":Output tokens: {metadata['usage']['outputTokens']}")
                    print(f":Total tokens: {metadata['usage']['totalTokens']}")
                    if 'cacheReadInputTokens' in metadata['usage']:
                        print(f"cacheReadInputTokens tokens: {metadata['usage']['cacheReadInputTokens']}")
                    if 'cacheWriteInputTokens' in metadata['usage']:
                        print(f"cacheWriteInputTokens tokens: {metadata['usage']['cacheWriteInputTokens']}")

                if 'metrics' in event['metadata']:
                    print(f"Latency: {metadata['metrics']['latencyMs']} milliseconds")
    return result
