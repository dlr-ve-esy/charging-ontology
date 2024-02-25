# %%
import requests
from pathlib import Path

VERSION = "v1.9.5"
ROBOT_BASE = "https://github.com/ontodev/robot/releases/download/{}/robot.jar"
# Change this path according to your setup.
ROBOT_PATH = "../robot.jar"

# %%
if not Path(ROBOT_PATH).exists():
    with open(ROBOT_PATH, "wb") as local:
        response = requests.get(ROBOT_BASE.format(VERSION))
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {ROBOT_PATH} already exists, you are good to go.")
# %%
