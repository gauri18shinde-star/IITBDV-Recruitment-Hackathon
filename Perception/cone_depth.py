from ultralytics import YOLO
import cv2
import numpy as np

# -----------------------------
# Parameters (assumptions)
# -----------------------------
REAL_CONE_HEIGHT = 0.30   # meters 
FOCAL_LENGTH = 1000.0       # miliiimetres

IMAGE_PATH = "image.png"
OUTPUT_PATH = "output.png"
MODEL_PATH = "YOLOv11s-Carmaker.pt"   # trained YOLO cone model


# -----------------------------
# Load YOLO model
# -----------------------------
model = YOLO(MODEL_PATH)

# -----------------------------
# Run inference
# -----------------------------
results = model(IMAGE_PATH)

# Load image for drawing
img = cv2.imread(IMAGE_PATH)

detections = results[0].boxes.xyxy.cpu().numpy()

cone_distances = []

# -----------------------------
# Process detections
# -----------------------------
for i, box in enumerate(detections):

    x1, y1, x2, y2 = box.astype(int)

    # Bounding box height
    pixel_height = y2 - y1

    if pixel_height <= 0:
        continue

    # Depth calculation
    distance = (REAL_CONE_HEIGHT * FOCAL_LENGTH) / pixel_height
    cone_distances.append(distance)

    # Draw bounding box
   # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 153, 204), 2)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    cv2.circle(img,(cx,cy),4,(0,0,255),-1)

    label = f"{distance:.2f}m"

    # Draw label
    cv2.putText(
        img,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_COMPLEX,
        0.6,
        (0, 0, 0),
        2
    )

# -----------------------------
# Save output image
# -----------------------------
cv2.imwrite(OUTPUT_PATH, img)

# -----------------------------
# Print results
# -----------------------------
print("Detected Cones and Estimated Distances:\n")

for i, d in enumerate(cone_distances):
    print(f"Cone {i+1}: {d:.2f} meters")

print(f"\nAnnotated image saved as: {OUTPUT_PATH}")