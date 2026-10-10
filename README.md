# YourPose-CNN-Reproducibility-Materials
Selected reproducibility materials for the YourPose-CNN head pose estimation research

1) Overview

This repository provides selected reproducibility materials associated with the research work on YourPose-CNN, a head pose estimation framework combining face-region processing, mask-guided learning, pose classification, and continuous pose regression.

The purpose of this repository is to document selected aspects of the experimental protocol and provide the materials currently authorized for public release.

2) Materials Available

The following materials are provided in this repository:

a) Dataset split manifests: Lists of image filenames assigned to the training, validation, and testing sets.


b) Subject-disjoint verification: A script to verify subject separation across the training, validation, and testing sets, based on the identifiers available in the manifests.


c) Rotation matrix-to-angle conversion: Code describing the conversion of rotation matrices into yaw, pitch, and roll angles.


d) Head pose classification labels: Code implementing the rules used to assign the seven discrete pose labels: L, LU, LD, R, RU, RD, and N.


3) Materials Not Currently Released

The complete model-training code and model-evaluation code are not included in this public repository. Their release is currently restricted.

4) Reproducibility Scope and Limitations

The currently available files support inspection of selected dataset-splitting procedures, subject-disjoint verification, angle conversion, and discrete pose-label assignment. They do not, by themselves, provide a complete end-to-end reproduction of model training, evaluation, or computational benchmarking.

5) The repository will be updated if additional materials are authorized for release.

