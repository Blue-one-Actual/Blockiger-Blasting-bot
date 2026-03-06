import argparse
import logging
import threading
import time

from vision import capture_frame, find_best_block_position
from input_controller import click_at
import safety


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run"), default="dry-run")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
    stop_event = threading.Event()
    safety.init_stop_handlers(stop_event)

    logging.info("Starting bot in %s mode", args.mode)
    try:
        while not stop_event.is_set():
            frame = capture_frame()
            pos = find_best_block_position(frame)
            if pos is None:
                logging.debug("No valid block position detected")
            else:
                x, y, conf = pos
                logging.info("Detected pos=(%s,%s) conf=%.2f", x, y, conf)
                if args.mode == "run" and conf > 0.5:
                    click_at(x, y, stop_event)
            time.sleep(0.1)
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    finally:
        logging.info("Bot stopped")


if __name__ == "__main__":
    main()
