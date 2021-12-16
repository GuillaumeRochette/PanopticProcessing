import argparse
from pathlib import Path

from metadata import SEQUENCES, SUBSEQUENCES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "python database_masks.py"

    for sequence, subsequences in zip(SEQUENCES, SUBSEQUENCES):
        videos = sorted((root / sequence / "Masks" / "SOLO").glob("*"))
        for video in videos:
            cmd = f"{executable} --sequence={root / sequence} --video_name={video.name} --subsequences='{subsequences}'"
            print(cmd)


if __name__ == '__main__':
    main()
