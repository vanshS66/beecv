"""Detect and label coloured blocks from a webcam feed."""

from __future__ import annotations

import argparse
from collections.abc import Iterator

import cv2
import numpy as np


# HSV handles lighting changes better than direct BGR comparisons. Red wraps the
# hue scale, so it needs two ranges. Tune these values for the local lighting.
COLOUR_RANGES: dict[str, tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...]] = {
    "red": (((0, 100, 70), (10, 255, 255)), ((170, 100, 70), (180, 255, 255))),
    "orange": (((11, 100, 70), (25, 255, 255)),),
    "yellow": (((26, 100, 70), (35, 255, 255)),),
    "green": (((36, 70, 50), (85, 255, 255)),),
    "blue": (((86, 100, 50), (130, 255, 255)),),
    "purple": (((131, 70, 50), (169, 255, 255)),),
}

DRAW_COLOURS: dict[str, tuple[int, int, int]] = {
    "red": (0, 0, 255), "orange": (0, 140, 255), "yellow": (0, 255, 255),
    "green": (0, 255, 0), "blue": (255, 0, 0), "purple": (255, 0, 255),
}


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Detect coloured blocks from a camera feed.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0).")
    parser.add_argument(
        "--min-area", type=int, default=1_000,
        help="Ignore detections smaller than this many pixels (default: 1000).",
    )
    return parser.parse_args()


def contours_for_colour(hsv_frame: np.ndarray, colour: str) -> Iterator[np.ndarray]:
    """Yield contours belonging to one named colour."""
    mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
    for lower, upper in COLOUR_RANGES[colour]:
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv_frame, np.array(lower), np.array(upper)))

    kernel = np.ones((5, 5), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yield from contours


def annotate_blocks(frame: np.ndarray, min_area: int) -> np.ndarray:
    """Return a copy of *frame* annotated with each detected colour block."""
    annotated = frame.copy()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for colour in COLOUR_RANGES:
        for contour in contours_for_colour(hsv_frame, colour):
            if cv2.contourArea(contour) < min_area:
                continue
            x, y, width, height = cv2.boundingRect(contour)
            cv2.rectangle(annotated, (x, y), (x + width, y + height), DRAW_COLOURS[colour], 2)
            cv2.putText(annotated, colour, (x, max(y - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, DRAW_COLOURS[colour], 2, cv2.LINE_AA)
    return annotated


def main() -> None:
    """Open the selected camera and display labelled colour blocks."""
    args = parse_args()
    camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened():
        raise RuntimeError(
            f"Could not open camera {args.camera}. "
            "Check the index and ensure no other application is using it."
        )

    window_name = "BeeCV colour blocks - press q or Esc to quit"
    try:
        while True:
            success, frame = camera.read()
            if not success:
                raise RuntimeError("Could not read a frame from the camera.")
            cv2.imshow(window_name, annotate_blocks(frame, args.min_area))
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
