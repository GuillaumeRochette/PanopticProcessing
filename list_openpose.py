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

    executable = f"bash {skeleton}.docker.sh"

    for sequence in SEQUENCES:
        videos = sorted((root / sequence / "Videos").glob("*.mp4"))
        for video in videos:
            view, suffix = video.stem, ".tar.xz"
            poses = root / sequence / "Poses" / "2D" / skeleton / (view + suffix)
            cmd = f"{executable} {video} {poses}"
            print(cmd)


if __name__ == '__main__':
    main()
