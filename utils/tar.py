import json
import re
import tarfile
import io

from tqdm import tqdm


def extract(path, pattern="([0-9]{12})+"):
    pattern = re.compile(pattern)
    d = {}
    with tarfile.open(path) as tar:
        for name in tqdm(tar.getnames()):
            match = pattern.search(name)
            if match:
                key = match[0]
                value = tar.extractfile(name).read()
                value = json.loads(value)
                d[key] = value
    return d


def compress(path, d):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    suffix = path.suffix.split(".")[-1]
    dir_name = path.stem.split(".")[0]
    with tarfile.open(path, f"w:{suffix}") as tar:
        for key, value in tqdm(d.items()):
            data = json.dumps(value)

            tarinfo = tarfile.TarInfo(f"{dir_name}/{key}.json")
            tarinfo.size = len(data)
            tar.addfile(tarinfo, io.BytesIO(data.encode()))
