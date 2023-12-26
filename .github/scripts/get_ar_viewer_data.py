import json
import os
import shutil

from utils import (download_and_extract_zip, get_dict_from_js_var,
                   get_dict_from_json)
from validation import is_valid_ar_viewer_dict


def get_added_and_deleted_items(extracted_names: set, website_names: set, items_extracted: list, items_website: list) -> (str, set, set):
    """
    Checks if the items in two lists are equal.

    Args:
        extracted_names (set): The names of the extracted items.
        website_names (set): The names of the website items.
        items_extracted (list): The extracted items.
        items_website (list): The website items.

    Returns:
        str: The changes made. It could be additions, removals or updates.
        set: The added items.
        set: The deleted items.
    """
    changes_made = ""
    added_items = extracted_names - website_names
    deleted_items = website_names - extracted_names
    for item_name in added_items:
        changes_made += f"\t{item_name} added (AR Viewer App Database)\n"
    for item_name in deleted_items:
        changes_made += f"\t{item_name} deleted (AR Viewer App Database)\n"
    return changes_made, added_items, deleted_items


def check_added_variants(item_extracted: dict, item_website: dict, item_name: str) -> str:
    """
    Check for added variants in an item.

    Args:
        item_extracted (dict): The extracted item.
        item_website (dict): The item from the website.
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
            changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}' has been added (AR Viewer App Database)\n"
    return changes_made


def check_updated_or_deleted_variants(item_extracted: dict, item_website: dict, item_name: str) -> str:
    """
    Check for updated or deleted variants in an item.

    Args:
        item_extracted (dict): The extracted item.
        item_website (dict): The item from the website.
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
            changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}' has been deleted (AR Viewer App Database)\n"
        else:
            for variant_key, variant_value in variant_extracted.items():
                if variant_value != variant_website.get(variant_key):
                    changes_made += f"\tIn {item_name}'s family, the variant '{variant_name}'s {variant_key} has been updated, from '{
                        variant_website.get(variant_key)}' to '{variant_value}' (AR Viewer App Database)\n"
    return changes_made


def check_item_variants(item_extracted: dict, item_website: dict, item_name: str) -> str:
    """
    Check variants of an item for updates or additions.

    Args:
        item_extracted (dict): The extracted item.
        item_website (dict): The item from the website.
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
    return changes_made


def update_changes_made_about_variants(items_extracted: list, items_website: list, deleted_items: set, added_items: set) -> str:
    """
    Checks if the variants in two lists are equal.

    Args:
        items_extracted (list): The extracted items.
        items_website (list): The website items.
        deleted_items (set): The deleted items.
        added_items (set): The added items.

    Returns:
        str: The changes made. It could be additions, removals or updates.
    """
    changes_made = ""
    for item_extracted in items_extracted:
        item_name = item_extracted.get('product_name')
        if item_name not in deleted_items and item_name not in added_items:
            item_website = next((item for item in items_website if item.get('product_name') == item_name), None)
            if item_website is not None:
                changes_made += check_item_variants(item_extracted, item_website, item_name)
    return changes_made


def update_changes_made_about_data(json_file_extracted: dict, json_file_website: dict) -> str:
    """
    Checks if two JSON files are equal.

    Args:
        json_file_extracted (Dict): The extracted JSON file.
        json_file_website (Dict): The JSON file from the website.

    Returns:
        str: The changes made. It could be additions, removals or updates.
    """
    changes_made = ""
    items_extracted = json_file_extracted.get('items')
    items_website = json_file_website.get('items')
    extracted_names = set(item['product_name'] for item in items_extracted)
    website_names = set(item['product_name'] for item in items_website)
    changes_mades_about_data, added_items, deleted_items = get_added_and_deleted_items(extracted_names, website_names, items_extracted, items_website)
    changes_made_about_variants = update_changes_made_about_variants(items_extracted, items_website, deleted_items, added_items)
    changes_made += changes_mades_about_data + changes_made_about_variants
    return changes_made


def update_changes_made_about_imgs(image_folder_extracted: str, image_folder_website: str) -> (str, set):
    """
    Checks if the images in two folders are equal.

    Args:
        image_folder_extracted (str): The path to the extracted image folder.
        image_folder_website (str): The path to the website image folder.

    Returns:
        str: The changes made. It could be additions, removals or updates.
        set: The images to update.
    """
    changes_made = ""
    img_to_update = set()
    for img_name in os.listdir(image_folder_extracted):
        img_extracted = os.path.join(image_folder_extracted, img_name)
        img_website = os.path.join(image_folder_website, img_name)
        if not os.path.isfile(img_website):
            img_to_update.add(img_name)
            changes_made += f"\tAdded {img_name} to img folder (AR Viewer App Database)\n"
        elif (os.path.getsize(img_extracted) != os.path.getsize(img_website)):
            img_to_update.add(img_name)
            changes_made += f"\tUpdated {img_name} in img folder (AR Viewer App Database)\n"
    return changes_made, img_to_update


def update_imgs(image_folder_extracted: str, image_folder_website: str, img_to_update: set) -> None:
    """
    Updates the images in the website.

    Args:
        image_folder_extracted (str): The path to the extracted image folder.
        image_folder_website (str): The path to the website image folder.
        zip_name (str): The name of the ZIP file.
        extracted_path (str): The path to the extracted ZIP file.

    Returns:
        None
    """
    for img_name in img_to_update:
        img_extracted = os.path.join(image_folder_extracted, img_name)
        img_website = os.path.join(image_folder_website, img_name)
        with open(img_extracted, "rb") as f:
            with open(img_website, "wb") as f1:
                f1.write(f.read())


def update_ar_viewer_data() -> None:
    """
    Update the RobotStudio AR Viewer App data.
    It's getting the data from the RobotStudio AR Viewer App, and then it's comparing it with the data in the repo.
    If there's any changes, it will update the data in the repo.
    And then it will return the changes made to log it and be written in a releases_notes.txt file.

    Returns:
        str: The changes made. It could be additions, removals or updates.
    """
    extracted_path = "./extracted"
    url_zip = "https://xrhayesstoragetest.blob.core.windows.net/libraries/robots_db_prod.zip"
    zip_name = os.path.basename(url_zip)
    changes_made = ""
    image_extracted_folder_path = os.path.join(extracted_path, "img")
    image_website_folder_path = os.path.join("assets", "img", "abb_images")
    download_and_extract_zip(url_zip, extracted_path)
    json_file_website = get_dict_from_js_var(os.path.join("assets", "scripts", "inlineJson.js"), "myJson")
    json_file_extracted = get_dict_from_json(os.path.join(extracted_path, "database.json"))
    if not is_valid_ar_viewer_dict(json_file_extracted):
        print("JSON file format is invalid")
        return None
    changes_made = update_changes_made_about_data(json_file_extracted, json_file_website)
    if changes_made:
        with open(os.path.join("assets", "scripts", "inlineJson.js"), "w") as f:
            f.write("var myJson = " + json.dumps(json_file_extracted) + ";")
    changes_made_about_img, img_to_update = update_changes_made_about_imgs(image_extracted_folder_path, image_website_folder_path)
    update_imgs(image_extracted_folder_path, image_website_folder_path, img_to_update)
    os.remove(zip_name)
    shutil.rmtree(extracted_path)
    changes_made += changes_made_about_img
    if changes_made != "":
        return changes_made


if __name__ == "__main__":
    print(update_ar_viewer_data())
