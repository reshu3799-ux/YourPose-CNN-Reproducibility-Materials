import os
import re
import shutil

# ============================================================
# GET INPUT FOLDER FROM USER
# ============================================================

input_folder = input(
    "Enter the path of the input image folder: "
).strip()

# Remove quotes if the user enters a quoted path
input_folder = input_folder.strip('"').strip("'")

# Check whether the input folder exists
if not os.path.isdir(input_folder):
    print("\nERROR: The specified input folder does not exist.")
    exit()

# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

output_folder = os.path.join(
    input_folder,
    "classified_images"
)

# ============================================================
# SEVEN CLASS FOLDERS
# ============================================================

classes = [
    "N",
    "L",
    "R",
    "LU",
    "RU",
    "LD",
    "RD"
]

# Create all class folders
for class_name in classes:

    class_folder = os.path.join(
        output_folder,
        class_name
    )

    os.makedirs(
        class_folder,
        exist_ok=True
    )

print("\nOutput folder created:")
print(output_folder)

# ============================================================
# REGULAR EXPRESSION
#
# Example:
# 01_frame_00366_rgb_F0_Y1.71_P31.16_R-2.03.png
#
# Extract:
# Yaw   = 1.71
# Pitch = 31.16
# Roll  = -2.03
# ============================================================

pattern = re.compile(
    r"_Y(-?\d+(?:\.\d+)?)"
    r"_P(-?\d+(?:\.\d+)?)"
    r"_R(-?\d+(?:\.\d+)?)"
)

# ============================================================
# CLASSIFICATION FUNCTION
# ============================================================

def classify_pose(yaw, pitch):

    # --------------------------------------------------------
    # 1. N - Neutral
    #
    # IMPORTANT:
    # If yaw is between -20 and +20,
    # classify as N REGARDLESS OF PITCH.
    # --------------------------------------------------------

    if -20 < yaw < 20:
        return "N"

    # --------------------------------------------------------
    # 2. L - Left
    #
    # yaw <= -20
    # -20 < pitch < +20
    # --------------------------------------------------------

    elif yaw <= -20 and -20 < pitch < 20:
        return "L"

    # --------------------------------------------------------
    # 3. R - Right
    #
    # yaw >= +20
    # -20 < pitch < +20
    # --------------------------------------------------------

    elif yaw >= 20 and -20 < pitch < 20:
        return "R"

    # --------------------------------------------------------
    # 4. LU - Left + Up
    #
    # yaw <= -20
    # pitch <= -20
    # --------------------------------------------------------

    elif yaw <= -20 and pitch <= -20:
        return "LU"

    # --------------------------------------------------------
    # 5. RU - Right + Up
    #
    # yaw >= +20
    # pitch <= -20
    # --------------------------------------------------------

    elif yaw >= 20 and pitch <= -20:
        return "RU"

    # --------------------------------------------------------
    # 6. LD - Left + Down
    #
    # yaw <= -20
    # pitch >= +20
    # --------------------------------------------------------

    elif yaw <= -20 and pitch >= 20:
        return "LD"

    # --------------------------------------------------------
    # 7. RD - Right + Down
    #
    # yaw >= +20
    # pitch >= +20
    # --------------------------------------------------------

    elif yaw >= 20 and pitch >= 20:
        return "RD"

    # --------------------------------------------------------
    # Should never occur for valid yaw/pitch values
    # --------------------------------------------------------

    else:
        return None


# ============================================================
# SUPPORTED IMAGE EXTENSIONS
# ============================================================

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff"
)

# ============================================================
# COUNTERS
# ============================================================

total_images = 0
classified_images = 0
skipped_images = 0

class_counts = {
    "N": 0,
    "L": 0,
    "R": 0,
    "LU": 0,
    "RU": 0,
    "LD": 0,
    "RD": 0
}

# ============================================================
# PROCESS ALL IMAGES
# ============================================================

for filename in os.listdir(input_folder):

    # Ignore non-image files
    if not filename.lower().endswith(image_extensions):
        continue

    total_images += 1

    # --------------------------------------------------------
    # EXTRACT YAW, PITCH AND ROLL
    # --------------------------------------------------------

    match = pattern.search(filename)

    if match is None:

        print(
            f"SKIPPED - Cannot extract Y/P/R: "
            f"{filename}"
        )

        skipped_images += 1
        continue

    # Convert extracted values to float
    yaw = float(match.group(1))
    pitch = float(match.group(2))
    roll = float(match.group(3))

    # --------------------------------------------------------
    # CLASSIFY IMAGE
    # --------------------------------------------------------

    class_name = classify_pose(
        yaw,
        pitch
    )

    # --------------------------------------------------------
    # CHECK CLASS
    # --------------------------------------------------------

    if class_name is None:

        print(
            f"SKIPPED - No class found: "
            f"{filename} | "
            f"Yaw={yaw}, "
            f"Pitch={pitch}, "
            f"Roll={roll}"
        )

        skipped_images += 1
        continue

    # --------------------------------------------------------
    # DESTINATION FOLDER
    # --------------------------------------------------------

    destination_folder = os.path.join(
        output_folder,
        class_name
    )

    # --------------------------------------------------------
    # DESTINATION FILE
    # --------------------------------------------------------

    destination_path = os.path.join(
        destination_folder,
        filename
    )

    # --------------------------------------------------------
    # COPY IMAGE
    # --------------------------------------------------------

    shutil.copy2(
        os.path.join(input_folder, filename),
        destination_path
    )

    # --------------------------------------------------------
    # UPDATE COUNTERS
    # --------------------------------------------------------

    classified_images += 1
    class_counts[class_name] += 1

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print(
        f"{filename} --> {class_name} | "
        f"Yaw={yaw}, "
        f"Pitch={pitch}, "
        f"Roll={roll}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("CLASSIFICATION COMPLETED")
print("=" * 60)

print(
    f"Total images found : {total_images}"
)

print(
    f"Classified images  : {classified_images}"
)

print(
    f"Skipped images     : {skipped_images}"
)

print("\nClass-wise image count:")
print("-" * 30)

for class_name in classes:

    print(
        f"{class_name:>2} : "
        f"{class_counts[class_name]}"
    )

print("-" * 30)

print("\nImages saved in:")
print(output_folder)

print("=" * 60)
