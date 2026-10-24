"""Minimal OpenCV webcam preview application."""

from __future__ import annotations

import argparse

import cv2


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Show a live OpenCV camera preview.")
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index to open (default: 0).",
    )
    return parser.parse_args()


def main() -> None:
    """Open the selected camera and display frames until q or Esc is pressed."""
    args = parse_args()
    camera = cv2.VideoCapture(args.camera)

    if not camera.isOpened():
        raise RuntimeError(
            f"Could not open camera {args.camera}. "
            "Check the index and ensure no other application is using it."
        )

    window_name = "BeeCV - press q or Esc to quit"
    try:
        while True:
            success, frame = camera.read()
            if not success:
                raise RuntimeError("Could not read a frame from the camera.")

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):  # q or Escape
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
