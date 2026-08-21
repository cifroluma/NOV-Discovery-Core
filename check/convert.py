import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIGANDS_DIR = os.path.join(BASE_DIR, "ligands")

COUNT = 27610  # колхозно

os.makedirs(LIGANDS_DIR, exist_ok=True)

with open("generate.csv", mode="r", newline="") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for id, row in enumerate(csv_reader):  # Теперь row — это словарь
        smiles = row["SMILES"]
        out_pdbqt = os.path.join(LIGANDS_DIR, f"ligand{id}.pdbqt")
        temp_sdf = os.path.join(LIGANDS_DIR, f"temp_{id}.sdf")  # Временный файл

        # Шаг 1: Из SMILES делаем 3D структуру с водородами и минимизируем. Сохраняем в .sdf
        os.system(
            f'obabel -:"{smiles}" -O {temp_sdf} --gen3d -h --minimize --ff MMFF94'
        )

        # Шаг 2: Берем готовое 3D и перегоняем в .pdbqt с нужными зарядами
        os.system(f"obabel {temp_sdf} -O {out_pdbqt} --partialcharge Gasteiger")

        # Удаляем временный файл, чтобы не засорять папку
        if os.path.exists(temp_sdf):
            os.remove(temp_sdf)

        print(f"ГОТОВО {id}/{COUNT}")


print("КОНЕЦ")
