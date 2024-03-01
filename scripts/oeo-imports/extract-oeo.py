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
