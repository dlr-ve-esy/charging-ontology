# SPDX-FileCopyrightText: Copyright (c) 2024 German Aerospace Center (DLR)
# SPDX-License-Identifier: BSD-3-Clause
# %%
import subprocess as sp
from pathlib import Path
import os

CWD = Path(os.getcwd())
FILEPATH = Path(os.path.dirname(os.path.realpath(__file__)))

# Clunky search for the basedir
if FILEPATH == CWD:
    BASEDIR = Path("../..")
elif "VERSION" in [p.name for p in CWD.iterdir()]:
    BASEDIR = Path(".")
# %%
ROBOT_PATH = BASEDIR.joinpath("robot.jar")
TMP = BASEDIR.joinpath("tmp")
TMP.mkdir(exist_ok=True)


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
        jar=ROBOT_PATH.resolve().as_posix(),
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
    TMP.joinpath("ao_infrastructure.ttl"), TMP.joinpath("ao_infrastructure.owx")
)
robot_convert(BASEDIR.joinpath("src/imports/bfo-core.ttl"), TMP.joinpath("bfo.owx"))
robot_convert(TMP.joinpath("oeo_vehicle.ttl"), TMP.joinpath("oeo_vehicle.owx"))
robot_convert(TMP.joinpath("ao_vehicles.ttl"), TMP.joinpath("ao_vehicles.owx"))
robot_convert(
    TMP.joinpath("oeo_vehicle_ev_tax.ttl"), TMP.joinpath("oeo_vehicle_ev_tax.owx")
)
robot_convert(
    TMP.joinpath("oeo_vehicle_lv_tax.ttl"), TMP.joinpath("oeo_vehicle_lv_tax.owx")
)
# %%
