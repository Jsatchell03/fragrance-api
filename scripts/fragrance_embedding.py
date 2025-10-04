import pandas as pd
import numpy as np
import json
from openai import OpenAI
import time
import os
from dotenv import load_dotenv


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

df = pd.read_csv("../data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=False)
df = df_sorted
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
w_top, w_mid, w_base = 0.25, 0.30, 0.45
w_notes, w_accords = 0.6, 0.4

data = []
accord_columns = [
    "mainaccord1",
    "mainaccord2",
    "mainaccord3",
    "mainaccord4",
    "mainaccord5",
]


def embed_text(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(response.data[0].embedding)


def accord_vector(accords):
    if not accords:
        return np.zeros(1536)  # embedding dimension

    weights = np.linspace(
        len(accords), 1, num=len(accords)
    )  # main accord 1 gets highest weight
    weights = weights / weights.sum()  # normalize to sum to 1

    vecs = [embed_text(accord) for accord in accords]
    vecs = np.array(vecs)
    weighted_vec = np.sum(vecs * weights[:, np.newaxis], axis=0)
    return weighted_vec


def average_embeddings(texts, weight=1.0):
    if not texts:
        return np.zeros(1536)  # dimension of text-embedding-3-small
    vecs = [embed_text(t) for t in texts]
    avg = np.mean(vecs, axis=0)
    return weight * avg


start_time = time.time()
# Only add top 1000 bc time
for index, row in df.iterrows():
    if index < 1000:
        row_dict = row.to_dict()
        res = {}
        res["name"] = row_dict["Perfume"]
        res["brand"] = row_dict["Brand"]
        res["gender"] = row_dict["Gender"]
        res["country"] = row_dict["Country"]
        res["topNotes"] = [x.strip() for x in row_dict["Top"].split(",") if x.strip()]
        res["midNotes"] = [
            x.strip() for x in row_dict["Middle"].split(",") if x.strip()
        ]
        res["baseNotes"] = [x.strip() for x in row_dict["Base"].split(",") if x.strip()]
        res["accords"] = [
            row[col]
            for col in accord_columns
            if pd.notna(row[col]) and str(row[col]).strip()
        ]
        # Vectors
        res["topNotesVector"] = average_embeddings(res["topNotes"]).tolist()
        res["midNotesVector"] = average_embeddings(res["midNotes"]).tolist()
        res["baseNotesVector"] = average_embeddings(res["baseNotes"]).tolist()

        # Weighted total notes vector
        res["totalNotesVector"] = (
            w_top * np.array(res["topNotesVector"])
            + w_mid * np.array(res["midNotesVector"])
            + w_base * np.array(res["baseNotesVector"])
        ).tolist()

        res["accordsVector"] = accord_vector(res["accords"]).tolist()
        res["fragranceVector"] = (
            (w_notes * np.array(res["totalNotesVector"]))
            + (w_accords * np.array(res["accordsVector"]))
        ).tolist()
        data.append(res)
    else:
        break

with open("../data/embedded_frags.json", "w") as f:
    json.dump(data, f, indent=4)

end_time = time.time()
elapsed = end_time - start_time
print(f"Embedding took {elapsed:.2f} seconds")
