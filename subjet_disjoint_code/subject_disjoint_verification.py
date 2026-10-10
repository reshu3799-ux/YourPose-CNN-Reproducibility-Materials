import os

base_path = "path to folder which contains train.txt, validation.txt and test.txt"

file_paths = {
    "Training": os.path.join(base_path, "train.txt"),
    "Testing": os.path.join(base_path, "test.txt"),
    "Validation": os.path.join(base_path, "validation.txt")
}


def extract_subject_id(filename):
   
    filename = os.path.basename(filename.strip())

    if not filename:
        return None

    subject_id = filename.split("_")[0]

    return subject_id if subject_id.isdigit() else None


def read_subjects(txt_path):

    if not os.path.isfile(txt_path):
        raise FileNotFoundError(f"File not found: {txt_path}")

    subjects = set()
    invalid_filenames = []

    with open(txt_path, "r", encoding="utf-8") as file:
        for line in file:
            filename = line.strip()

            if not filename:
                continue

            subject_id = extract_subject_id(filename)

            if subject_id is None:
                invalid_filenames.append(filename)
            else:
                subjects.add(subject_id)

    return subjects, invalid_filenames


subject_sets = {}

for dataset_name, txt_path in file_paths.items():
    subjects, invalid_files = read_subjects(txt_path)
    subject_sets[dataset_name] = subjects

    print(f"\n{dataset_name}")
    print(f"Number of unique subjects: {len(subjects)}")
    print(f"Subject IDs: {sorted(subjects, key=int)}")

    if invalid_files:
        print("WARNING: Invalid filenames found:")
        for filename in invalid_files:
            print(f"  {filename}")


print("\n" + "=" * 65)
print("SUBJECT-DISJOINT VERIFICATION")
print("=" * 65)

pairs = [
    ("Training", "Testing"),
    ("Training", "Validation"),
    ("Testing", "Validation")
]

all_disjoint = True

for dataset_a, dataset_b in pairs:
    common_subjects = (
        subject_sets[dataset_a] & subject_sets[dataset_b]
    )

    print(f"\n{dataset_a} vs {dataset_b}")

    if common_subjects:
        all_disjoint = False
        print("FAIL: Subject overlap detected!")
        print("Common subject IDs:",
              sorted(common_subjects, key=int))
    else:
        print("PASS: No common subjects.")


print("\n" + "=" * 65)

if all_disjoint:
    print("FINAL RESULT: PASS")
    print("Training, Testing, and Validation are subject-disjoint.")
    print("No subject appears in more than one dataset.")
else:
    print("FINAL RESULT: FAIL")
    print("Subject overlap exists between datasets.")
    print("Review the common subject IDs reported above.")

print("=" * 65)

