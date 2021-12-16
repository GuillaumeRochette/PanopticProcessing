PanopticProcessing
===
---
### Requirements

1. Install Docker and follow post-installation steps: https://docs.docker.com/engine/install/
2. Install NVIDIA Docker: https://github.com/NVIDIA/nvidia-docker
3. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
4. Set-up the following environment:
```bash
conda create -n processing-env python=3.9 pip
conda activate processing-env
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
pip install lmdb tqdm
```
Note: Regarding the OpenPose and SOLOv2 parts, if you are using a GPU (which is recommended), its CUDA Compute Capability must be >= 5.0 and <=8.0, otherwise these Docker images might not work. 

### Overview
Here's how the file structure should look like:
```
/path/to/datasets/
├─ panoptic-toolbox/
│  ├─ 171026_pose1/
│  ├─ .../
├─ Panoptic/
│  ├─ 171026_pose1/
│  ├─ .../

/path/to/projects/
├─ PanopticProcessing/
├─ OpenPose/
├─ Reconstruction3D/
├─ SOLOv2/

```

### 1. Clone the Side Repositories
```bash
git clone https://github.com/GuillaumeRochette/OpenPose.git /path/to/projects/OpenPose
git clone https://github.com/GuillaumeRochette/SOLOv2.git /path/to/projects/SOLOv2
git clone https://github.com/GuillaumeRochette/Reconstruction3D.git /path/to/projects/Reconstruction3D
```

### 2. Download the Original Dataset
```bash
git clone https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox.git /path/to/datasets/panoptic-toolbox
cd panoptic-toolbox
./scripts/getData.sh 171026_pose1 0 31
./scripts/getData.sh 171026_pose2 0 31
./scripts/getData.sh 171026_pose3 0 31
./scripts/getData.sh 171204_pose1 0 31
./scripts/getData.sh 171204_pose2 0 31
./scripts/getData.sh 171204_pose3 0 31
./scripts/getData.sh 171204_pose4 0 31
./scripts/getData.sh 171204_pose5 0 31
./scripts/getData.sh 171204_pose6 0 31
```
### 3. Clean the Original Dataset
```bash
python cleanup.py --src_root=/path/to/datasets/panoptic-toolbox --dst_root=/path/to/datasets/Panoptic
```

### 4. Run OpenPose BODY_135 for 2D Poses
```bash
python list_openpose.py --root=/path/to/datasets/Panoptic > /path/to/projects/OpenPose/list_openpose.sh
cd /path/to/projects/OpenPose
bash list_openpose.sh
```

### 5. Run SOLOv2 for Segmentation Masks
```bash
python list_solov2.py --root=/path/to/datasets/Panoptic > /path/to/projects/SOLOv2/list_solov2.sh
cd /path/to/projects/SOLOv2
bash list_solov2.sh
```

### 6. Run Reconstruction3D for 3D Poses
```bash
python list_reconstruction_3d.py --root=/path/to/datasets/Panoptic > /path/to/projects/Reconstruction3D/list_reconstruction_3d.sh
cd /path/to/projects/Reconstruction3D
bash list_reconstruction_3d.sh
```

### 7. Make Databases
```bash
python list_database_images.py --root=/path/to/datasets/Panoptic > list_database_images.sh
bash list_database_images.sh

python list_database_masks.py --root=/path/to/datasets/Panoptic > list_database_masks.sh
bash list_database_masks.sh
 
python list_database_poses_2d.py --root=/path/to/datasets/Panoptic > list_database_poses_2d.sh
bash list_database_poses_2d.sh

python list_database_poses_3d.py --root=/path/to/datasets/Panoptic > list_database_poses_3d.sh
bash list_database_poses_3d.sh
```

### 8. Make Symlinks for Cameras
```bash
python symlinks_cameras.py --root=/path/to/datasets/Panoptic
```
