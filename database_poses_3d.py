import argparse
from pathlib import Path
import shutil
import pickle
import lmdb
from time import time
from tqdm import tqdm

import torch

from utils.tar import extract


def BODY_135(x):
    x = x["pose_keypoints_3d"]
    x = torch.tensor(x, dtype=torch.float32).reshape(-1, 4, 1)
    return x


def OpenPose(x):
    x = (
        x["pose_keypoints_3d"]
        + x["hand_left_keypoints_3d"][1 * 4 :]
        + x["hand_right_keypoints_3d"][1 * 4 :]
        + x["face_keypoints_3d"]
    )
    x = torch.tensor(x, dtype=torch.float32).reshape(-1, 4, 1)
    return x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence", type=Path, required=True)
    parser.add_argument("--poses_3d_name", type=str, required=True)
    parser.add_argument("--subsequences", type=str, required=True)
    parser.add_argument("--skeleton", type=str, default="BODY_135")
    args = parser.parse_args()

    sequence = args.sequence
    poses_3d_name = args.poses_3d_name
    subsequences = eval(args.subsequences)
    skeleton = args.skeleton

    if skeleton == "BODY_135":
        f = BODY_135
    elif skeleton == "OpenPose":
        f = OpenPose
    else:
        raise ValueError(f"Unknown skeleton: {skeleton}")

    poses_3d_path = sequence / "Poses" / "3D" / skeleton / poses_3d_name

    assert poses_3d_path.exists()

    poses_3d = {}
    for key, value in extract(poses_3d_path).items():
        if len(value["people"]) == 1:
            key = int(key)
            value = f(value["people"][0])
            poses_3d[key] = value

    # Make temporary directories.
    tmp_dir = Path("/tmp") / f"TEMP_{time()}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    for i, (start, end) in enumerate(subsequences):
        stem = poses_3d_name.split(".")[0]

        tmp_database = tmp_dir / f"{stem}.lmdb"

        # Remove any existing database.
        database = sequence / "Subsequences" / f"{i}" / "Databases" / "Poses" / "3D" / skeleton / f"{stem}.lmdb"
        database.parent.mkdir(parents=True, exist_ok=True)
        if database.exists():
            shutil.rmtree(database)
        print(database)

        indexes = [index for index in sorted(poses_3d.keys()) if start <= index <= end]
        shifted_indexes = [index - start for index in indexes]

        # Create the database.
        with lmdb.open(path=f"{tmp_database}", map_size=2 ** 40) as env:
            # Add the poses to the database.
            for index, shifted_index in zip(tqdm(indexes), shifted_indexes):
                with env.begin(write=True) as txn:
                    key = pickle.dumps(shifted_index)
                    value = pickle.dumps(poses_3d[index])
                    txn.put(key=key, value=value, dupdata=False)
            # Add the keys to the database.
            with env.begin(write=True) as txn:
                key = pickle.dumps("keys")
                value = pickle.dumps(shifted_indexes)
                txn.put(key=key, value=value, dupdata=False)
            # Add the protocol to the database.
            with env.begin(write=True) as txn:
                key = "protocol".encode("ascii")
                value = pickle.dumps(pickle.DEFAULT_PROTOCOL)
                txn.put(key=key, value=value, dupdata=False)

        # Move the database to its destination.
        shutil.move(f"{tmp_database}", database.parent)

    # Remove the temporary directories.
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
