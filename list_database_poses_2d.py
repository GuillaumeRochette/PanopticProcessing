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

    executable = "python database_poses_2d.py"

    for sequence, subsequences in zip(SEQUENCES, SUBSEQUENCES):
        poses_2ds = sorted((root / sequence / "Poses" / "2D" / skeleton).glob("*"))
        for poses_2d in poses_2ds:
            cmd = f"{executable} --sequence={root / sequence} --poses_2d_name={poses_2d.name} --subsequences='{subsequences}' --skeleton={skeleton}"
            print(cmd)


if __name__ == '__main__':
    main()
