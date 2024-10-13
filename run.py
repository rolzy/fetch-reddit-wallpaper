# Fetch wallpapers from Reddit.
# Using subreddit r/wallpaper and r/WidescreenWallpaper
# Features:
# - Fetch the hottest wallpaper each week
# - Keep 50 wallpapers in widescreen and 1080p
# - Delete old wallpapers FIFO
# - Wallpapers that do not have naming convention are kept (rename favourite pics to avoid deletion)

import logging
import os

import praw
from dotenv import load_dotenv

from src import fetch_wallpapers, remove_old_pics

USER_AGENT = (
    f"linux:com.example.wallpaper-fetch:v1.0 (by u/{os.getenv('REDDIT_USERNAME')})"
)

# Initialize logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=USER_AGENT,
)

if __name__ == "__main__":
    logging.info("Start fetching wallpaper")

    # Fetch wallpapers
    fetch_wallpapers(reddit)

    # Remove old ones
    remove_old_pics()
