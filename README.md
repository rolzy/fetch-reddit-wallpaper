# fetch-reddit-wallpaper

Automatically fetch a new wallpaper every using the Reddit API.

## Setup
1. Install Python (developed on 3.11.2)
2. I recommend creating a virtual environment (`python -m venv env && source env/bin/activate`)
3. Install Python packages `pip install -r requirements.txt`
4. Edit `config.json` with configuration for your system. You can set the resolution of your monitors, the image save location and the subreddit to source the wallpapers from. 
5. Run `python run.py`
6. Set your OS to display desktop wallpapers from the image save location
7. (Optional) Setup a cronjob to get a new wallpaper at your desired frequency

## Features
- Download the top weekly wallpaper from subreddit(s) specified in `config.json`
- Save the image in location specified in `config.json`
- Remove old images from the specified location if the number of images exceed a certain amount
    - The default number of images to retain is 50
    - If there are more than 50 images, the oldest image with the default naming convention is deleted
    - To avoid an image being deleted, rename the image so it doesn't have the default naming convention
