import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "dock_res")
ligands = os.listdir(PATH)  # ['','',]

i = 0
for ligand in ligands:
    with open(f"{PATH}/{ligand}", "r") as f:
        cont = f.readlines()

        for k, line in enumerate(cont):
            if line.startswith("ATOM"):
                t_s1 = line.split()[5]
                try:
                    t_s2 = cont[k + 1].split()[5]
                except IndexError:
                    print(t_s2)
                    break

                if t_s1 == t_s2:
                    os.remove(f"{PATH}/{ligand}")
                    i += 1
                    print(f"УДАЛЕНО {i}")
                    break

print("ГОТОВО")
