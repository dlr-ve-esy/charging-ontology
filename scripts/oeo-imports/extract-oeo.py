# %%
import requests
import subprocess as sp
from pathlib import Path

BASE_IRI = "http://openenergy-platform.org/ontology"
# http://openenergy-platform.org/ontology/oeo/releases/2.1.0/iao-imports.omn
# http://openenergy-platform.org/ontology/oeo/releases/2.1.0/oeo-physical.omn
# http://openenergy-platform.org/ontology/oeo/releases/2.1.0/imports/iao-extracted.owl
VERSION = "2.1.0"
ONTOLOGY_BASE = "http://openenergy-platform.org/ontology/oeo/releases/{}/{}"
UPPER_TERM = "http://purl.obolibrary.org/obo/BFO_0000003"
CLASS_IRI = "http://purl.obolibrary.org/obo/BFO_0000144"

TERM_FILE = "oeo-w-hierarchy.txt"
# Change these paths according to your setup.
ROBOT_PATH = "../../robot.jar"
IAO = "../../src/imports/iao-extracted.ttl"
TARGET = "../../src/imports/cco-extracted.ttl"
Path("tmp").mkdir(exist_ok=True)
# %%
# Get IAO imports
if not Path(IAO).exists():
    with open(IAO, "wb") as local:
        response = requests.get(
            ONTOLOGY_BASE.format(VERSION, "imports/iao-extracted.owl")
        )
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {IAO} already exists, you are good to go.")
# %% [markdown]
# Acquire the OEO Physical modules.
# %%
OEO_PHYSICAL_TEMP = "tmp/oeo-physical.omn"
if not Path(OEO_PHYSICAL_TEMP).exists():
    with open(OEO_PHYSICAL_TEMP, "wb") as local:
        response = requests.get(ONTOLOGY_BASE.format(VERSION, "oeo-physical.omn"))
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {OEO_PHYSICAL_TEMP} already exists, you are good to go.")
# %%
IAO_DROPPED = "iao-dropped.txt"
if Path(IAO).exists():
    extract_call = 'java -jar {jar} \
remove --input {input}  \
--term-file {term_file} \
--select "self" \
--exclude-term http://purl.obolibrary.org/obo/BFO_0000031 \
--output {output}'

    sp.call(
        extract_call.format(
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            input=Path(IAO).resolve().as_posix(),
            term_file=IAO_DROPPED,
            output=Path(IAO).resolve().as_posix(),
        ),
        shell=True,
    )

# %%
