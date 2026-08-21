import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "ligands")

ligands = os.listdir(PATH)  # ['','',]

with open("result.csv", mode="r", newline="") as csv_file:
    ligand_need = []
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        ligand_need.append(row[0])

for ligand in ligands:
    if not (ligand in ligand_need):
        os.remove(f"{PATH}/{ligand}")

print("ГОТОВО")
