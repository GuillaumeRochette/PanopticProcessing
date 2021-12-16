import argparse
from pathlib import Path
import json

import numpy as np

from metadata import SEQUENCES


def symlink(src_path: Path, dst_path: Path):
    print(src_path, dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        dst_path.unlink()
    dst_path.symlink_to(src_path.resolve())


def cameras(src_path: Path, dst_path: Path):
    print(src_path, dst_path)
    with src_path.open() as file:
        calibration = json.load(file)

    raw_cameras = [c for c in calibration["cameras"] if c["type"] == "hd"]
    cameras = {}
    for raw_camera in raw_cameras:
        view = raw_camera["name"].replace("00_", "")

        cameras[view] = {
            "R": np.array(raw_camera["R"]).tolist(),
            "t": (np.array(raw_camera["t"]) * 1e-2).tolist(),
            "K": np.array(raw_camera["K"]).tolist(),
            "dist_coef": np.array(raw_camera["distCoef"]).tolist(),
            "resolution": np.array(raw_camera["resolution"]).tolist(),
        }

    with dst_path.open("w") as file:
        json.dump(cameras, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_root", type=Path, required=True)
    parser.add_argument("--dst_root", type=Path, required=True)
    args = parser.parse_args()

    src_root = args.src_root
    dst_root = args.dst_root

    for sequence in SEQUENCES:
        src_sequence = src_root / sequence
        dst_sequence = dst_root / sequence

        for src_video in sorted((src_sequence / "hdVideos").glob("*.mp4")):
            stem, suffix = src_video.stem, src_video.suffix
            view = stem.replace("hd_00_", "")

            if sequence in ["171204_pose5", "171204_pose6"]:
                if view in ["12", "16", "18", "27"]:
                    # These videos are corrupted, which causes the extrinsic and intrinsic parameters to change over time.
                    continue

            symlink(
                src_path=src_video,
                dst_path=dst_sequence / "Videos" / (view + suffix),
            )

        symlink(
            src_path=src_sequence / "hdPose3d_stage1_coco19.tar",
            dst_path=dst_sequence / "Poses" / "3D" / "Panoptic" / "hdPose3d_stage1_coco19.tar",
        )
        symlink(
            src_path=src_sequence / "hdHand3d.tar",
            dst_path=dst_sequence / "Poses" / "3D" / "Panoptic" / "hdHand3d.tar",
        )
        symlink(
            src_path=src_sequence / "hdFace3d.tar",
            dst_path=dst_sequence / "Poses" / "3D" / "Panoptic" / "hdFace3d.tar",
        )

        cameras(
            src_path=src_sequence / f"calibration_{sequence}.json",
            dst_path=dst_sequence / "cameras.json",
        )


if __name__ == "__main__":
    main()
