import argparse
from pathlib import Path

from metadata import SEQUENCES, SUBSEQUENCES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--skeleton", type=str, default="BODY_135")
    args = parser.parse_args()

    root = args.root
    skeleton = args.skeleton

    executable = "python database_poses_3d.py"

    for sequence, subsequences in zip(SEQUENCES, SUBSEQUENCES):
        poses_3d = root / sequence / "Poses" / "3D" / skeleton / "Reconstructed.tar.xz"
        cmd = f"{executable} --sequence={root / sequence} --poses_3d_name={poses_3d.name} --subsequences='{subsequences}' --skeleton={skeleton}"
        print(cmd)


if __name__ == '__main__':
    main()
