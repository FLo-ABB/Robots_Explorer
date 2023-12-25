import requests
from json_compare_utils import get_dict_from_js_var
import os


def fetch_robodk_data() -> str:
    """
    Fetch the RoboDK data from the website.

    Returns:
        str: The RoboDK data.
    """
    url = "https://robodk.com/library-robots/bundlerdklib.js"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error occurred while fetching the RoboDK data: {e}")
    return response.text


def get_robodk_data(js_file_from_robodk: str) -> str:
    """
    Get the RoboDK data from the JS file.

    Args:
        js_file_from_robodk (str): The JS file from RoboDK.

    Returns:
        str: The RoboDK data.
    """
    text = js_file_from_robodk
    text = text[text.find("DATA_ALL:"):]
    text = text[text.find("{"):]
    number_of_open_brackets = 0
    number_of_closed_brackets = 0
    for i in range(len(text)):
        if text[i] == "{":
            number_of_open_brackets += 1
        elif text[i] == "}":
            number_of_closed_brackets += 1
        if number_of_open_brackets == number_of_closed_brackets:
            return text[:i+1]
        else:
            continue
    return None


def update_changes_made(old_data: dict, new_data: dict) -> None:
    """
    Update the changes made.

    Args:
        changes_made (str): The changes made.

    Returns:
        None
    """
    changes_made = ""
    # check if if keys has been removed
    for robot in old_data.keys():
        if robot not in new_data.keys():
            changes_made += f"\t'{robot}' has been removed (RoboDK)\n"
    # check if keys has been added
    for robot in new_data.keys():
        if robot not in old_data.keys():
            changes_made += f"\t'{robot}' has been added (RoboDK)\n"
    # check if keys has been updated
    for robot in new_data.keys():
        if robot in old_data.keys():
            for key, value in new_data[robot].items():
                if value != old_data[robot].get(key):
                    changes_made += f"\t'{robot}'s {key} has been updated, from '{old_data[robot].get(key)}' to '{value} (RoboDK)'\n"
    return changes_made


def update_robodk_data() -> None:
    js_file_from_robodk = fetch_robodk_data()
    new_robodk_data = get_robodk_data(js_file_from_robodk)
    old_robodk_data = get_dict_from_js_var(os.path.join("assets", "scripts", "robodk_data.js"), "data")
    with open(os.path.join("assets", "scripts", "robodk_data.js"), "w") as f:
        f.write("var data = "+new_robodk_data+";")
    new_robodk_data = get_dict_from_js_var(os.path.join("assets", "scripts", "robodk_data.js"), "data")
    if new_robodk_data != old_robodk_data:
        return update_changes_made(old_robodk_data, new_robodk_data)
    else:
        return None


if __name__ == "__main__":
    print(update_robodk_data())
