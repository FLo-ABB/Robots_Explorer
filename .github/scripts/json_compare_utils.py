from typing import Dict
import json
from py_mini_racer import py_mini_racer


def check_item_variants(item_extracted: Dict, item_website: Dict, item_name: str) -> str:
    """
    Check variants of an item for updates or additions.

    Args:
        item_extracted (Dict): The extracted item.
        item_website (Dict): The item from the website.
        item_name (str): The name of the item.

    Returns:
        None
    """
    changes_made = ''
    for key, value in item_extracted.items():
        if key != 'product_name' and value != item_website.get(key):
            if key == 'variants':
                changes_made += check_added_variants(item_extracted, item_website, item_name)
                changes_made += check_updated_or_deleted_variants(item_extracted, item_website, item_name)
            else:
                changes_made += f"\tIn {item_name}, the {key} has been updated, from '{item_website.get(key)}' to '{value}'\n"
    return changes_made


def check_added_variants(item_extracted: Dict, item_website: Dict, item_name: str) -> str:
    """
    Check for added variants in an item.

    Args:
        item_extracted (Dict): The extracted item.
        item_website (Dict): The item from the website.
        item_name (str): The name of the item.

    Returns:
        None
    """
    changes_made = ''
    extracted_variants = item_extracted.get('variants')
    website_variants = item_website.get('variants')

    for variant_extracted in extracted_variants:
        variant_name = variant_extracted.get('name')
        variant_website = next((variant for variant in website_variants if variant.get('name') == variant_name), None)

        if variant_website is None:
            changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}' has been added\n"
    return changes_made


def check_updated_or_deleted_variants(item_extracted: Dict, item_website: Dict, item_name: str) -> str:
    """
    Check for updated or deleted variants in an item.

    Args:
        item_extracted (Dict): The extracted item.
        item_website (Dict): The item from the website.
        item_name (str): The name of the item.

    Returns:
        None
    """
    changes_made = ''
    extracted_variants = item_extracted.get('variants')
    website_variants = item_website.get('variants')

    for variant_website in website_variants:
        variant_name = variant_website.get('name')
        variant_extracted = next((variant for variant in extracted_variants if variant.get('name') == variant_name), None)

        if variant_extracted is None:
            changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}' has been deleted\n"
        else:
            for variant_key, variant_value in variant_extracted.items():
                if variant_value != variant_website.get(variant_key):
                    changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}'s {variant_key} has been updated,\
                          from '{variant_website.get(variant_key)}' to '{variant_value}'\n"
    return changes_made


def check_json_refactoring(json_file_extracted: Dict, json_file_website: Dict) -> str:
    """
    Check for JSON refactoring, i.e., if the JSON files do not have the same keys.

    Args:
        json_file_extracted (Dict): The extracted JSON file.
        json_file_website (Dict): The JSON file from the website.

    Returns:
        None
    """
    changes_made = ''
    if json_file_extracted.keys() != json_file_website.keys():
        global equality
        equality = False
        changes_made += "\tJSON refactoring\n"
    return changes_made


def get_json_from_js_var(js_file_path: str, var_name: str) -> dict:
    """
    Extracts a JSON object from a JavaScript file variable.

    Args:
        js_file_path (str): The path to the JavaScript file.
        var_name (str): The name of the JavaScript variable containing the JSON object.

    Returns:
        dict: The extracted JSON object.

    Raises:
        FileNotFoundError: If the JavaScript file does not exist.
        IndexError: If the JavaScript variable is not found in the file.
        json.JSONDecodeError: If there is an error decoding the JSON object.
    """
    try:
        with open(js_file_path, "r", encoding='utf-8') as f:
            json_file_string = f.read().split("var " + var_name + " = ")[1].split(";")[0]

        json_file = json.loads(json_file_string)
        return json_file

    except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
        print(f"Error occurred while extracting JSON object from JavaScript file: {e}")


def get_dict_from_js_var(js_file_path: str, var_name: str) -> dict:
    with open(js_file_path, "r") as f:
        data = f.read().split("var ")[1].split(";")[0]
    ctx = py_mini_racer.MiniRacer()
    ctx.execute(data)
    json_str = ctx.eval(f'JSON.stringify({var_name})')
    return json.loads(json_str)
