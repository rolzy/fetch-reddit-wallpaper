import glob
import json
import logging
import os

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
with open(os.path.join(parent_dir, "config.json"), "r") as config_file:
    MAPPING = json.load(config_file)


def remove_old_pics():
    for resolution, config in MAPPING.items():
        # List the files saved in item.get("image_save_location")
        image_save_location = config.get("image_save_location")
        if not image_save_location:
            logger.warning(f"No image save location found for {resolution}")
            continue

        # Check if there are more than 50 pics in the folder with the naming convention defined in get_wallpaper.py
        image_pattern = os.path.join(
            image_save_location, "[0-9][0-9]-[A-Z][a-z][a-z]-([0-9][0-9])_*"
        )
        image_files = glob.glob(image_pattern)

        if len(image_files) > 50:
            # If there are more than 50 pics, delete images with the naming convention, oldest first, until there are 50 pics
            image_files.sort(key=os.path.getctime)  # Sort by creation time
            files_to_delete = image_files[:-50]  # Keep the 50 newest files

            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted old wallpaper: {file_path}")
                except OSError as e:
                    logger.error(f"Error deleting file {file_path}: {e}")
            logger.info(
                f"Cleaned up wallpapers for {resolution}. Current count: {len(image_files)}"
            )
        else:
            logger.info(
                f"Not removing any wallpapers for {resolution}. Current count: {len(image_files)}"
            )
