import datetime
import json
import logging
import os
from io import BytesIO

import requests
from PIL import Image
from praw import Reddit

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
with open(os.path.join(parent_dir, "config.json"), "r") as config_file:
    MAPPING = json.load(config_file)


def check_image_resolution(image_data, expected_resolution):
    try:
        with Image.open(BytesIO(image_data)) as img:
            width, height = img.size
            return f"{width}x{height}" == expected_resolution
    except Exception as e:
        logger.error(f"Error checking image resolution: {e}")
        return False


def fetch_image(reddit_instance: Reddit, config: dict):
    resolution = config.get("resolution")
    subreddit = config.get("subreddit")
    image_save_location = config.get("image_save_location")

    for submission in reddit_instance.subreddit(subreddit).top(time_filter="week"):
        if resolution in submission.title:
            # Get the image URL from the reddit post
            url = submission.url

            # Skip galleries for now
            if "gallery" in url:
                continue

            # Create the file name
            file_extension = "." + url.split(".")[-1]
            weeknumber = datetime.datetime.now().strftime("(%U)")
            date = datetime.datetime.now().strftime("%d-%b-(%U)")
            image_name = submission.title.replace(" ", "_")
            filename = date + "_" + image_name + file_extension

            # If image_name already exist in folder, skip download
            # If image already downloaded for week, skip the entire process
            skip = False
            for file in os.listdir(image_save_location):
                if weeknumber in file:
                    logger.warning(
                        f"Image already downloaded for week {weeknumber.replace('(','').replace(')','')}, skipping..."
                    )
                    return
                if image_name in file:
                    logger.warning(
                        f"Image {image_name} already downloaded before, skipping..."
                    )
                    skip = True

            if skip:
                continue

            # Download the file
            logger.info(f"Downloading file {filename} from {url}")
            r = requests.get(url)

            # Check if the image resolution matches the expected resolution
            if check_image_resolution(r.content, resolution):
                with open(image_save_location + filename, "wb") as f:
                    f.write(r.content)
                logger.info(f"Image saved successfully: {filename}")
                break
            else:
                logger.warning(
                    f"Image resolution does not match {resolution}, skipping..."
                )
                continue


def fetch_wallpapers(reddit_instance: Reddit):
    for resolution, config in MAPPING.items():
        logger.info(f"Getting {resolution} wallpaper")
        fetch_image(reddit_instance, config)
