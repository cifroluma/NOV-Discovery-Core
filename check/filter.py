import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "dock_res")
center = (18.642, -3.125, 22.555)


for ligand in os.listdir(PATH):

    min_dist = float("inf")
    score = None

    with open(os.path.join(PATH, ligand), "r") as f:
        for line in f:
            if line.startswith("REMARK VINA RESULT:"):
                parts = line.split()
                if len(parts) >= 4:
                    score = float(parts[3])

            elif line.startswith("ATOM") or line.startswith("HETATM"):
                row = line.split()
                if "N" in row or "O" in row:
                    try:
                        atom_coords = (float(row[5]), float(row[6]), float(row[7]))

                        dist = math.dist(center, atom_coords)
                        if dist < min_dist:
                            min_dist = dist
                    except (ValueError, IndexError):
                        pass

    # Фильтруем: выводим только если есть скор, он мощнее -9.5 и дистанция <= 3.0 Å
    if score is not None and score <= -9.5 and min_dist <= 3.0:
        print(
            f"Кандидат: {ligand} | Скор: {score} | Дистанция до гема: {min_dist:.2f} Å"
        )
