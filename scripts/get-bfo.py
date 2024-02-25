# %%
import requests
from pathlib import Path

CCO_BFO_COMMIT = "d9aa636303766bfb6a7a6d46265873f96cdd8584"
ONTOLOGY_BASE = "https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/{}/imports/bfo-core.ttl"
# Change this path according to your setup.
TARGET = "../src/imports/bfo-core.ttl"
# %%
if not Path(TARGET).exists():
    with open(TARGET, "wb") as local:
        response = requests.get(ONTOLOGY_BASE.format(CCO_BFO_COMMIT))
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {TARGET} already exists, you are good to go.")
# %%
