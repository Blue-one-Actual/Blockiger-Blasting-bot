import logging
import os
import glob
import cv2
import numpy as np

try:
    import mss
except Exception:
    mss = None


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')


def capture_frame():
    """Capture the full screen and return an RGB numpy array.

    Uses `mss` for speed; falls back to an empty frame if unavailable.
    """
    if mss is not None:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            img = sct.grab(monitor)
            arr = np.array(img)
            # mss returns BGRA; convert to BGR or RGB depending on cv2 usage
            if arr.shape[2] == 4:
                arr = arr[:, :, :3]
            return cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    else:
        logging.warning("mss not available; returning placeholder frame")
        return np.zeros((1080, 1920, 3), dtype=np.uint8)


def _load_templates():
    """Load PNG templates from the `templates/` folder as grayscale arrays.

    Returns list of (name, image).
    """
    templates = []
    pattern = os.path.join(os.path.dirname(__file__), '..', 'templates', '*.png')
    for path in glob.glob(pattern):
        try:
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            name = os.path.splitext(os.path.basename(path))[0]
            templates.append((name, img))
        except Exception:
            logging.exception("Failed to load template %s", path)
    return templates


def find_best_block_position(frame, min_confidence=0.6):
    """Find best matching template position in `frame`.

    Returns (x_center, y_center, confidence) or None if no good match.
    """
    if frame is None:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    templates = _load_templates()
    if not templates:
        logging.debug("No templates found in %s", TEMPLATES_DIR)
        return None

    best = (None, 0.0, None)  # (name, confidence, top-left)
    for name, tpl in templates:
        try:
            res = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > best[1]:
                best = (name, float(maxVal), maxLoc)
        except Exception:
            logging.exception("Template matching failed for %s", name)

    if best[0] is None:
        return None

    name, conf, topleft = best
    # load template size for center calc
    tpl_path = os.path.join(os.path.dirname(__file__), '..', 'templates', f"{name}.png")
    tpl_img = cv2.imread(tpl_path, cv2.IMREAD_GRAYSCALE)
    h, w = tpl_img.shape[:2]
    x_center = topleft[0] + w // 2
    y_center = topleft[1] + h // 2

    if conf < min_confidence:
        logging.debug("Best match confidence %.2f below min %.2f", conf, min_confidence)
        return None

    return (int(x_center), int(y_center), conf)

