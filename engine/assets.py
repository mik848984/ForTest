import os
from settings import ASSETS_DIR


def get_asset_path(*paths):
    """Return absolute path to asset inside the assets directory."""
    return os.path.join(ASSETS_DIR, *paths)
