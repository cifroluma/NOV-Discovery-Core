import csv
import os
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "dock_res")
ligands = os.listdir(PATH)  # ['','',]

data = []
fieldnames = ["LIGAND_ID", "MARK"]

for ligand in tqdm(ligands):
    with open(f"{PATH}/{ligand}", "r") as f:
        next(f)
        target_string = next(f)

    target = float(target_string.split()[3])
    data.append({"LIGAND_ID": ligand, "MARK": target})

data.sort(key=lambda x: x["MARK"])

with open("result.csv", mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
