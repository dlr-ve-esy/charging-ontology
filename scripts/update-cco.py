from glob import glob
from pathlib import Path
with open("iri-mapping-v2.0.csv", "r") as f:
    header = f.readline()
    mapping = {l[0].strip(): l[1].strip() for l in [p.split(",") for p in f.readlines()]}



for g in glob("scripts/cco-imports/*.txt"):
    pth = Path(g)
    with open(pth, "r") as cf:
        lines = cf.readlines()
    with open(pth.parent / f"new-{pth.name}", "w") as new:
        for l in lines:
            if not ("BFO" in l):
                new.write(f"{mapping[l.strip()]}\n")
            else:
                new.write(f"{l.strip()}\n")