import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
import pubchempy as pcp
import ollama
import time
import sascorer
import re
import csv
import os

file_name = "generate.csv"

# Генератор в ollama
model_name = "qwen2.5:3b"
system_prompt = """You are an expert chemist. Your task is to generate NEW, VALID SMILES strings for drug-like molecules.
STRICT INSTRUCTIONS:
1. Output ONLY the SMILES string. NO text, NO markdown, NO explanations.
2. Do NOT start with "Here is...". Just the code.
3. Make complex structures (rings, halogens).

EXAMPLES:
Input: Generate one.
Output: CCN1C=CC(Br)=NC2=C1OC2

Input: Generate another.
Output: CC(C)C1=CC=C(C)C=C1NC(=O)CN2CCN(CC2)C3=CC=C(Cl)C=C3"""


def generate_smiles() -> list:
    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": "Next SMILES",
            },
        ],
        options={
            "num_predict": 128,
            "temperature": 1.5,
            "top_k": 100,
        },
    )
    return response["message"]["content"]


# И так понятно
def extract_smiles(text):
    text = text.replace("```", "").replace("`", "").strip()

    pattern = r"[CNOPSFIBrClHcnops1234567890\[\]()=\-\+@#%\\\/]{5,}"

    candidates = re.findall(pattern, text)
    if not candidates:
        return None

    smiles = max(candidates, key=len)

    smiles = re.sub(r"^[\d]+\.\s*", "", smiles)
    smiles = re.sub(r"^[\d]+\)\s*", "", smiles)
    smiles = smiles.lstrip(" .-*#")

    smiles = smiles.rstrip(". ;,:!?")

    return smiles


# Валидатор rdkit
def check_smiles(smiles: str) -> bool:
    if not smiles:
        return False

    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return False

    # Сначала считаем самые легкие параметры
    mwt = Descriptors.MolWt(m)
    if not (150 <= mwt < 600):
        return False

    # Если вес ок, считаем остальное
    logp = Descriptors.MolLogP(m)
    if not (1 <= logp <= 4):
        return False

    if Descriptors.NumHDonors(m) > 5:
        return False

    if Descriptors.NumHAcceptors(m) > 10:
        return False

    score = sascorer.calculateScore(m)
    if score > 5.2:
        return False

    # Фармакофорный фильтр: ищем азол/пиридин (ароматический азот в кольце)
    pharmacophore = Chem.MolFromSmarts("[n]")  # [n] - ароматический азот
    if not m.HasSubstructMatch(pharmacophore):
        return False

    return True


# Проверка на новизну: Стучится в PubChem.
def check_uniq(smiles: str) -> bool:
    try:
        if not pcp.get_cids(smiles):
            time.sleep(1)
            return True
    except:
        return False  # если ошибка сети
    return False


# main part
start_time = time.perf_counter()
count = 0
count_uniq_valid = 0

try:
    file_exists = os.path.isfile(file_name)

    csv_file = open(file_name, "a", newline="")
    writer = csv.writer(csv_file)

    if not file_exists:
        writer.writerow(["SMILES", "Weight", "LogP", "SA"])
        csv_file.flush()

    while True:
        # \r убираем, чтобы видеть историю. Будет спам, зато поймем ошибку.
        print(f"--- Итерация {count} ---")
        count += 1

        print("1. Генерирую...")
        raw_smiles = generate_smiles()
        smiles = extract_smiles(raw_smiles)

        print(f"2. Проверяю химию: {smiles}")
        if check_smiles(smiles):

            print(
                "3. Стучусь в PubChem..."
            )  # <--- ЕСЛИ ЗАВИСНЕТ ТУТ, ЗНАЧИТ БАН ПО IP ИЛИ ЛАГ
            if check_uniq(smiles):
                count_uniq_valid += 1

                print("4. Сохраняю...")
                m = Chem.MolFromSmiles(smiles)
                row = [
                    smiles,
                    round(Descriptors.MolWt(m), 2),
                    round(Descriptors.MolLogP(m), 2),
                    round(sascorer.calculateScore(m), 2),
                ]
                writer.writerow(row)
                csv_file.flush()
                print(f"[+] УСПЕХ! SMILES: {smiles}")
            else:
                print("[-] Не уникально (или ошибка сети)")
        else:
            print("[-] Химия не прошла")


except KeyboardInterrupt:
    end_time = time.perf_counter()
    res = end_time - start_time
    print(
        f"""
          Куда ты жмал... Конец. Результаты:
          За {res:.6f} секунд {count} попыток, из них афигенные {count_uniq_valid}.
          КПД: {count_uniq_valid/count}
          """
    )
    csv_file.close()
