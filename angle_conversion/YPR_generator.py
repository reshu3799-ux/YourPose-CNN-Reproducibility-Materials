import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# =========================
# INPUT / OUTPUT PATHS
# =========================
input_folder = "path to BIWI dataset folder containing frames subject wise"
output_folder = "path to save the detected faces with yaw,pitch and roll labels"

os.makedirs(output_folder, exist_ok=True)

# =========================
# INITIALIZE SCRFD (InsightFace)
# =========================
app = FaceAnalysis(name='buffalo_l')  # uses SCRFD detector
app.prepare(ctx_id=0)  # CPU mode

# =========================
# ROTATION MATRIX → YPR
# =========================
def rotationMatrixToEulerAngles(R):
    sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    singular = sy < 1e-6

    if not singular:
        pitch = np.arctan2(R[2,1], R[2,2])
        yaw   = np.arctan2(-R[2,0], sy)
        roll  = np.arctan2(R[1,0], R[0,0])
    else:
        pitch = np.arctan2(-R[1,2], R[1,1])
        yaw   = np.arctan2(-R[2,0], sy)
        roll  = 0

    return np.degrees(yaw), np.degrees(pitch), np.degrees(roll)

# =========================
# PROCESS IMAGES
# =========================
folder_name = os.path.basename(input_folder)

for file in sorted(os.listdir(input_folder)):

    if not file.endswith("_rgb.png"):
        continue

    image_path = os.path.join(input_folder, file)

    # Pose file
    pose_file = file.replace("_rgb.png", "_pose.txt")
    pose_path = os.path.join(input_folder, pose_file)

    if not os.path.exists(pose_path):
        print(f"Pose file missing for {file}")
        continue

    # =========================
    # READ IMAGE
    # =========================
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    # =========================
    # FACE DETECTION (SCRFD)
    # =========================
    faces = app.get(image)

    if len(faces) == 0:
        print(f"No face detected in {file}")
        continue

    # =========================
    # READ ROTATION MATRIX (same for all faces)
    # =========================
    with open(pose_path, "r") as f:
        lines = f.readlines()

    R = []
    for line in lines[:3]:
        values = list(map(float, line.strip().split()))
        R.append(values)

    R = np.array(R)

    yaw, pitch, roll = rotationMatrixToEulerAngles(R)

    yaw = round(yaw, 2)
    pitch = round(pitch, 2)
    roll = round(roll, 2)

    # =========================
    # PROCESS ALL FACES
    # =========================
    for idx, face_obj in enumerate(faces):

        x1, y1, x2, y2 = face_obj.bbox.astype(int)

        # Clamp to image boundaries
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        # Optional padding
        pad = 20
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w, x2 + pad)
        y2 = min(h, y2 + pad)

        face = image[y1:y2, x1:x2]

        if face.size == 0:
            print(f"Invalid crop in {file}, face {idx}")
            continue

        face = cv2.resize(face, (50, 50))

        # =========================
        # SAVE OUTPUT
        # =========================
        base_name = file.replace(".png", "")
        output_name = f"{folder_name}_{base_name}_F{idx}_Y{yaw}_P{pitch}_R{roll}.png"
        output_path = os.path.join(output_folder, output_name)

        cv2.imwrite(output_path, face)

        print(f"Saved: {output_name}")

print("\n✅ All faces processed successfully!")
