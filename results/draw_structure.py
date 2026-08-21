from rdkit import Chem
from rdkit.Chem import Draw

smiles = "OC[C@H]1CC[C@@H]1OCc2ccc(cc2)CCC2=CNC3=C(C=NN=C3)C=C2"

mol = Chem.MolFromSmiles(smiles)

if mol is None:
    raise ValueError("RDKit не смог распарсить SMILES")

img = Draw.MolToImage(mol, size=(600, 600))
img.save("structure_2d.png")
