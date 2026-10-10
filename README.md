# YourPose-CNN-Reproducibility-Materials
Selected reproducibility materials for the YourPose-CNN head pose estimation research

Overview

This repository provides selected reproducibility materials associated with the research work on YourPose-CNN, a head pose estimation framework combining face-region processing, mask-guided learning, pose classification, and continuous pose regression.

The purpose of this repository is to document selected aspects of the experimental protocol and provide the materials currently authorized for public release.

Materials Available

The following materials are provided in this repository:

Dataset split manifests: Lists of image filenames assigned to the training, validation, and testing sets.


Subject-disjoint verification: A script to verify subject separation across the training, validation, and testing sets, based on the identifiers available in the manifests.


Rotation matrix-to-angle conversion: Code describing the conversion of rotation matrices into yaw, pitch, and roll angles.


Head pose classification labels: Code implementing the rules used to assign the seven discrete pose labels: L, LU, LD, R, RU, RD, and N.


Materials Not Currently Released

The complete model-training code and model-evaluation code are not included in this public repository. Their release is currently restricted.

Reproducibility Scope and Limitations

The currently available files support inspection of selected dataset-splitting procedures, subject-disjoint verification, angle conversion, and discrete pose-label assignment. They do not, by themselves, provide a complete end-to-end reproduction of model training, evaluation, or computational benchmarking.

The repository will be updated if additional materials are authorized for release.

Usage

Please consult the relevant dataset documentation and the accompanying research publication when interpreting the split manifests, angle conventions, and pose-classification rules.

Contact

For questions about the available reproducibility materials, please refer to the corresponding research publication.
