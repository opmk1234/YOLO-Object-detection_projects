import cv2
import os

input_path = 'Cars/2.mp4'
output_path = os.path.join('Cars', '5.mp4')

# --- Open video ---
cap = cv2.VideoCapture(input_path)

if not cap.isOpened():
    print("Cannot open video file!")
    exit()

# --- Get video properties ---
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:  # fallback if OpenCV fails to read FPS
    fps = 30

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Original size: {width}x{height}, FPS: {fps}, Total frames: {frame_count}")

# --- Resize target ---
new_width, new_height = 1280, 720

# --- Create VideoWriter ---
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

frame_number = 0

# --- Process frames ---
while True:
    suc, frame = cap.read()
    if not suc or frame is None:
        print("Finished reading all frames.")
        break

    try:
        resized_frame = cv2.resize(frame, (new_width, new_height))
    except cv2.error:
        print(f"Skipping frame {frame_number} due to resize error.")
        continue

    out.write(resized_frame)

    frame_number += 1
    if frame_number % 50 == 0:  # progress every 50 frames
        print(f"Processing frame {frame_number}/{frame_count}")

# --- Release everything ---
cap.release()
out.release()
cv2.destroyAllWindows()

print("Video resized and saved successfully!")
print(f"Saved to: {os.path.abspath(output_path)}")
