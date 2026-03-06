"""Calibration tool: capture a frame, save sample and optionally save a template crop.

Usage:
    python tools/calibrate.py                # saves sample.png in repo root
    python tools/calibrate.py --save-template name --x 100 --y 200 --w 64 --h 64
"""
import argparse
import os
import sys
import numpy as np
# Ensure project root is on sys.path so relative imports work when running from tools/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT, 'src')
# Ensure src/ is on sys.path so imports like `from vision import ...` work
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from vision import capture_frame
try:
    from PIL import Image
except Exception:
    Image = None


def save_image_array(arr, path):
    if Image is None:
        print("Pillow not available; cannot save image")
        return False
    img = Image.fromarray(arr)
    img.save(path)
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--save-template", help="template name to save (saves to templates/<name>.png)")
    p.add_argument("--x", type=int, default=0)
    p.add_argument("--y", type=int, default=0)
    p.add_argument("--w", type=int, default=64)
    p.add_argument("--h", type=int, default=64)
    args = p.parse_args()

    frame = capture_frame()
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sample_path = os.path.join(root, 'sample.png')
    if isinstance(frame, np.ndarray):
        if save_image_array(frame, sample_path):
            print("Saved sample to", sample_path)
        else:
            print("Couldn't save sample (Pillow missing)")
    else:
        print("No frame captured")

    if args.save_template:
        tpl_dir = os.path.join(root, 'templates')
        os.makedirs(tpl_dir, exist_ok=True)
        x, y, w, h = args.x, args.y, args.w, args.h
        crop = frame[y:y+h, x:x+w]
        tpl_path = os.path.join(tpl_dir, f"{args.save_template}.png")
        if save_image_array(crop, tpl_path):
            print("Saved template to", tpl_path)
        else:
            print("Couldn't save template (Pillow missing)")


if __name__ == '__main__':
    main()
