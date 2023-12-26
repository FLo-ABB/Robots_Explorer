import json
import os
import zipfile
from json import JSONDecodeError

import requests
from py_mini_racer import py_mini_racer


def download_and_extract_zip(zip_url: str, extracted_path: str) -> None:
    """
    Downloads and extracts a ZIP file from the given URL to the specified path.

    Args:
        zip_url (str): The URL of the ZIP file to download.
        extracted_path (str): The path to extract the ZIP file.

    Returns:
        None

    Raises:
        requests.RequestException: If there is an error in the HTTP request.
        zipfile.BadZipFile: If the downloaded file is not a valid ZIP file.
        zipfile.LargeZipFile: If the extracted ZIP file exceeds ZIP file size limits.
        FileNotFoundError: If the extracted path does not exist.
    """
    zip_name = os.path.basename(zip_url)
    download_zip(zip_url, zip_name)
    extract_zip(zip_name, extracted_path)


def download_zip(url: str, destination: str) -> None:
    """
    Downloads a ZIP file from the given URL to the specified path.

    Args:
        url (str): The URL of the ZIP file to download.
        destination (str): The path to download the ZIP file.

    Returns:
        None

    Raises:
        requests.RequestException: If there is an error in the HTTP request.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(destination, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error occurred while downloading the ZIP file: {e}")


def extract_zip(zip_path: str, extracted_path: str) -> None:
    """
    Extracts a ZIP file from the given path to the specified path.

    Args:
        zip_path (str): The path of the ZIP file to extract.
        extracted_path (str): The path to extract the contents of the ZIP file.

    Returns:
        None

    Raises:
        zipfile.BadZipFile: If the downloaded file is not a valid ZIP file.
        zipfile.LargeZipFile: If the extracted ZIP file exceeds ZIP file size limits.
        FileNotFoundError: If the extracted path does not exist.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_path)
    except (zipfile.BadZipFile, zipfile.LargeZipFile, FileNotFoundError) as e:
        print(f"Error occurred while extracting the ZIP file: {e}")


def has_required_keys(keys: list, element: list) -> bool:
    """
    Checks if the given element contains all the required keys.

    Args:
        keys (list): The required keys.
        element (list): The element to check.

    Returns:
        bool: True if the element contains all the required keys, False otherwise.
    """
    return all(key in element for key in keys)


def get_dict_from_js_var(js_file_path: str, var_name: str) -> dict:
    try:
        with open(js_file_path, "r") as f:
            data = f.read().split("var ")[1].split(";")[0]
        ctx = py_mini_racer.MiniRacer()
        ctx.execute(data)
        json_str = ctx.eval(f'JSON.stringify({var_name})')
        return json.loads(json_str)
    except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
        print(f"Error occurred while extracting JSON object from JavaScript file: {e}")


def get_dict_from_json(json_file_path: str) -> dict:
    """
    Converts a JSON file to a Python dictionary.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        dict: The Python dictionary.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except JSONDecodeError as e:
        print(f"Error occurred while decoding JSON file: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error occurred while opening JSON file: {e}")
        return None
