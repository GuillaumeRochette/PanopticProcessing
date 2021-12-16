import argparse
from pathlib import Path

from metadata import SEQUENCES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "bash run_video.docker.sh"

    for sequence in SEQUENCES:
        videos = sorted((root / sequence / "Videos").glob("*.mp4"))
        for src_video in videos:
            dst_video = root / sequence / "Masks" / "SOLO" / src_video.name
            cmd = f"{executable} {src_video} {dst_video}"
            print(cmd)


if __name__ == '__main__':
    main()
