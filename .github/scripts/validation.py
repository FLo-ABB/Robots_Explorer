import json

from utils import has_required_keys


def is_valid_ar_viewer_dict(json_obj: json) -> bool:
    """
    Validate if the dict from the RobotStudio AR Viewer App follows the expected format.

    Args:
        json_obj (dict): JSON object to validate.

    Returns:
        bool: True if the JSON object is valid, False otherwise.
    """
    item_keys = ["product_name", "product_thumb", "tittle", "description", "read_more_url", "product_type",
                 "controller", "variants"]
    variant_keys = ["name", "capacity", "reach"]
    if "items" not in json_obj:
        return False
    if not all(has_required_keys(item_keys, item) for item in json_obj["items"]):
        return False
    if not all(has_required_keys(variant_keys, variant) for item in json_obj["items"] for variant in item["variants"]):
        return False
    return True
