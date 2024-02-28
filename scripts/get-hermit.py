# %%
import requests
from pathlib import Path

HERMIT = "https://github.com/owlcs/releases/raw/master/HermiT/org.semanticweb.hermit-packaged-1.4.6.519-SNAPSHOT.jar "
# Change this path according to your setup.
HERMIT_PATH = "../hermit.jar"

# %%
if not Path(HERMIT_PATH).exists():
    with open(HERMIT_PATH, "wb") as local:
        response = requests.get(HERMIT)
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {HERMIT_PATH} already exists, you are good to go.")
# %%
