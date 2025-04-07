"""Tool to downsize images."""

import argparse
import logging
import os
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def get_args() -> dict:
    argparse.ArgumentParser(description="Downsize an image")
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="path to image")
    parser.add_argument("--root-folder", action=argparse.BooleanOptionalAction)
    parser.add_argument("--log-level", type=str, default="INFO", help="log level")
    parser.add_argument("--overwrite", action=argparse.BooleanOptionalAction)
    ret_dict: dict = {
        "path": parser.parse_args().path,
        "root-folder": parser.parse_args().root_folder,
        "log-level": parser.parse_args().log_level,
        "overwrite": parser.parse_args().overwrite,
    }
    return ret_dict


def downsize(path: str, overwrite: bool = False) -> None:
    img: Image = Image.open(path)
    img = img.resize((300, 300), Image.LANCZOS)
    if overwrite:
        logger.info(f"Overwriting {path}")
        img.save(path, optimize=True, quality=95)
    else:
        path = Path(path)
        path = path.parent / Path(path.stem + "_downsized" + path.suffix)
        logger.info(f"Write {path}")
        img.save(path, optimize=True, quality=95)


def main() -> None:
    args: dict = get_args()
    path: str = args["path"]
    overwrite: bool = args["overwrite"]

    if args["log-level"] == "INFO":
        logging.basicConfig(level=logging.INFO)

    if bool(args["root-folder"]):
        # TODO: Use pathlib with glob
        files = [
            os.path.join(dp, f)
            for dp, dn, filenames in os.walk(path)
            for f in filenames
            if os.path.splitext(f)[1] in [".jpeg", ".jpg", ".png"]
        ]
        for e in files:
            logger.info(f"Downsizing {e}")
            downsize(e, overwrite)
    else:
        downsize(path, overwrite)


if __name__ == "__main__":
    main()
