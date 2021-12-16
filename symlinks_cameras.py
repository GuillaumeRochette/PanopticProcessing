import argparse
from pathlib import Path

from metadata import SEQUENCES, SUBSEQUENCES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    for sequence, subsequences in zip(SEQUENCES, SUBSEQUENCES):
        src_cameras = root / sequence / "cameras.json"
        for i, (_, _) in enumerate(subsequences):
            dst_cameras = root / sequence / "Subsequences" / f"{i}" / "cameras.json"
            print(src_cameras, dst_cameras)
            if dst_cameras.exists():
                dst_cameras.unlink()
            dst_cameras.symlink_to(src_cameras.resolve())


if __name__ == '__main__':
    main()
