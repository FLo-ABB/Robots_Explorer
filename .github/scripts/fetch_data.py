from get_robodk_data import update_robodk_data
from get_ar_viewer_data import update_ar_viewer_data
import datetime
import os


def add_changes_made_to_file(changes_made: str, file_path: str) -> None:
    """
    Adds the changes made to a file.

    Args:
        changes_made (str): The changes made.
        file_path (str): The path to the file to write to.

    Returns:
        None
    """
    with open(file_path, "r") as f:
        content = f.read()
    with open(file_path, "w") as f:
        f.write(changes_made + content)


def main() -> None:
    """

    """
    robodk_changes = update_robodk_data()
    ar_viewer_changes = update_ar_viewer_data()
    if robodk_changes or ar_viewer_changes:
        changes_made = f"-{datetime.datetime.now().strftime('%Y-%m-%d')}: \n"
        if robodk_changes:
            changes_made += robodk_changes
        if ar_viewer_changes:
            changes_made += ar_viewer_changes
        add_changes_made_to_file(changes_made, os.path.join("assets", "release_notes.txt"))


if __name__ == "__main__":
    main()
