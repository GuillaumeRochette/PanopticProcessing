import argparse
from pathlib import Path

from metadata import SEQUENCES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--skeleton", type=str, default="BODY_135")
    args = parser.parse_args()

    root = args.root
    skeleton = args.skeleton

    executable = f"python {skeleton}.py"

    for sequence in SEQUENCES:
        poses_2d_dir = root / sequence / "Poses" / "2D" / skeleton
        calibration = root / sequence / "cameras.json"
        poses_3d = root / sequence / "Poses" / "3D" / skeleton / "Reconstructed.tar.xz"
        cmd = f"{executable} --poses_2d_dir={poses_2d_dir} --calibration={calibration} --poses_3d={poses_3d}"
        print(cmd)


if __name__ == '__main__':
    main()
