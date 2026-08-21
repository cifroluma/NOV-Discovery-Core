import os
import subprocess
from tqdm import tqdm
import concurrent.futures

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIGANDS_DIR = os.path.join(BASE_DIR, "ligands")
OUTPUT_DIR = "dock_res"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def docking(ligand: str):
    process = subprocess.Popen(
        [
            "vina",
            "--batch",
            os.path.join(LIGANDS_DIR, ligand),
            "--config",
            "config.txt",
            "--dir",
            OUTPUT_DIR,
        ]
    )

    return_code = process.wait()


ligands = os.listdir(LIGANDS_DIR)  # ['','',]


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        # map сам раскидает файлы из списка по свободным потокам
        futures = [executor.submit(docking, ligand) for ligand in ligands]

        for _ in tqdm(
            concurrent.futures.as_completed(futures), total=len(ligands), desc="Фигачим"
        ):
            pass


if __name__ == "__main__":
    main()
