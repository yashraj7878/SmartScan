import re
import constants
import os
import requests
import pandas as pd
import multiprocessing
import time
from time import time as timer
from tqdm import tqdm
import numpy as np
from pathlib import Path
from functools import partial
import urllib
from PIL import Image

def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def parse_string(s):
    s_stripped = "" if s is None or str(s) == 'nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError(f"Invalid format in {s}")
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in constants.allowed_units:
        raise ValueError(f"Invalid unit [{unit}] found in {s}. Allowed units: {constants.allowed_units}")
    return number, unit

def create_placeholder_image(image_save_path):
    """Creates a black placeholder image for failed downloads."""
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        pass

def download_image(image_link, save_folder, retries=3, delay=3):
    """Downloads a single image and handles failures."""
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):  # Skip already downloaded images
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except:
            time.sleep(delay)

    create_placeholder_image(image_save_path)  # Placeholder for invalid links

def download_images(image_links, download_folder, limit=100000, allow_multiprocessing=True):
    """Downloads up to `limit` images from the provided links."""
    
    # Ensure the folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Select only `limit` unique images
    unique_links = list(set(image_links))[:limit]  # Limit the number of downloads

    if allow_multiprocessing:
        download_image_partial = partial(download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(32) as pool:
            list(tqdm(pool.imap(download_image_partial, unique_links), total=len(unique_links)))
            pool.close()
            pool.join()
    else:
        for image_link in tqdm(unique_links, total=len(unique_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)
