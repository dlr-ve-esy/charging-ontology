# %%
import requests
import subprocess as sp
from pathlib import Path

# %%
ROBOT_PATH = "../../robot.jar"
TMP = "tmp"
Path(TMP).mkdir(exist_ok=True)


# %%
def robot_convert(
    input: str,
    output: str,
    formt: str = "owx",
):
    """Call robot to do a convertion"""
    convert_call = (
        "java -jar {jar} merge "
        "--input {input} convert "
        "--output {output} "
        "--format {formt}"
    )
    debug_string = convert_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        output=Path(output).resolve().as_posix(),
        formt=formt,
    )
    code = sp.call(
        debug_string,
        shell=True,
    )
    if code != 0:
        print(debug_string)
        raise IOError(f"Something went wrong with call: {debug_string}")
    return code


# %%
robot_convert(
    "../cco-imports/tmp/ao_infrastructure.ttl", f"{TMP}/ao_infrastructure.owx"
)
robot_convert("../../src/imports/bfo-core.ttl", f"{TMP}/bfo.owx")
robot_convert("../oeo-imports/tmp/oeo_vehicle.ttl", f"{TMP}/oeo_vehicle.owx")
robot_convert("../cco-imports/tmp/ao_vehicles.ttl", f"{TMP}/ao_vehicles.owx")
robot_convert(
    "../oeo-imports/tmp/oeo_vehicle_lv_tax.ttl", f"{TMP}/oeo_vehicle_lv_tax.owx"
)
# %%
