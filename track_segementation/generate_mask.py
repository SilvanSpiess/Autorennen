import cv2
import numpy as np

IMAGE_TRACK = 'resources/rennstrecke.png'
IMAGE_FENCE = 'resources/rennstrecke_marked_fence_removed_bushes.png'

MASK_TRACK = 'resources/rennstrecke_mask_track.png'
MASK_FENCE = 'resources/rennstrecke_mask_fence.png'

# [Hue, Saturation, Value]
FILTER_TRACK_LOWER = np.array([0, 0, 50])
FILTER_TRACK_HIGHER = np.array([10, 10, 200])

FILTER_FENCE_LOWER = np.array([0, 0, 0])
FILTER_FENCE_HIGHER = np.array([1, 1, 1])

DO_TRACK = False
DO_FENCE = True

if DO_TRACK:
    image = cv2.imread(IMAGE_TRACK)

    # Convert from BGR to HSV color space (easier to filter colors)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create the initial mask (Track becomes White, everything else Black)
    track_mask = cv2.inRange(hsv, FILTER_TRACK_LOWER, FILTER_TRACK_HIGHER)

    # Clean up noise (fences or small details on the track) using Morphology
    kernel = np.ones((5, 5), np.uint8)
    # Closing fills in small black holes (like fences/cars) inside the white track
    track_mask = cv2.morphologyEx(track_mask, cv2.MORPH_CLOSE, kernel)
    # Opening removes tiny white specks outside the track area
    track_mask = cv2.morphologyEx(track_mask, cv2.MORPH_OPEN, kernel)

    # Save the finished mask
    cv2.imwrite(MASK_TRACK, track_mask)
    print(f"Mask generated successfully as {MASK_TRACK}!")

if DO_FENCE:
    image = cv2.imread(IMAGE_FENCE)

    # Convert from BGR to HSV color space (easier to filter colors)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create the initial mask (Track becomes White, everything else Black)
    track_mask = cv2.inRange(hsv, FILTER_FENCE_LOWER, FILTER_FENCE_HIGHER)

    # Save the finished mask
    cv2.imwrite(MASK_FENCE, track_mask)
    print(f"Mask generated successfully as {MASK_FENCE}!")