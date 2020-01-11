import numpy as np
import pandas as pd
import re
from glob import glob
from os import path

dfs = []
for fp in glob("webscraper/json/*.json"):
    with open(fp, 'r') as f:
        dfs.append(pd.read_json(f))

def trim_name(s):
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s

def get_paths(s):
    paths = []
    for data in s:
        relpath = data["path"]
        abspath = path.join(path.dirname(path.realpath(__file__)), "webscraper/images", relpath)
        paths.append(abspath)
    return paths

for i in range(len(dfs)):
    dfs[i]['name_latin'] = dfs[i]['name_latin'].apply(trim_name)
    dfs[i]['images'] = dfs[i]['images'].apply(get_paths)
    dfs[i] = dfs[i].drop(["image_urls"],axis=1)

def fillna_emptylist(df, col):
    isnull = df[col].isnull()
    df.loc[isnull, col] = [[]] * isnull.sum()
    return df

# merge all dataframes on latin name
df = dfs.pop()
while len(dfs):
    df = pd.merge(df, dfs.pop(), on="name_latin", how="outer")
    # hack to merge missing lists
    df = fillna_emptylist(df, "images_x")
    df = fillna_emptylist(df, "images_y")
    df["images"] = df["images_x"] + df["images_y"]
    df = df.drop(["images_x","images_y"], axis=1)

# filter only ones with finnish name for now
df = df[df["name_fi"].notna()]
df[["name_fi","name_latin","images"]].to_json("aggregated.json", orient='records')