# %%
import requests
from pathlib import Path
import subprocess as sp
import os
ONTOLOGY_BASE = (
    "https://enterpriseintegrationlab.github.io/icity/Parking/doc/ontology.ttl"
)
# Change this path according to your setup.

CWD = Path(os.getcwd())
FILEPATH = Path(os.path.dirname(os.path.realpath(__file__)))

# Clunky search for the basedir
if FILEPATH == CWD:
    BASEDIR = Path("../..")
elif "VERSION" in [p.name for p in CWD.iterdir()]:
    BASEDIR = Path(".")

TMP = BASEDIR.joinpath("tmp")
TMP.mkdir(exist_ok=True)
ROBOT_PATH = BASEDIR.joinpath("robot.jar")

INPUT = BASEDIR.joinpath("src/edits/chio-core.ttl")


# %%
    
def load_terms(term_file):
    with open(term_file, "r") as terms:
        term_list = [l for l in terms.readlines()]
    return term_list

def extract_subset(input: str, output: str, terms: str):
    """Call robot to do a subset extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method subset "
        "--term-file {term_file} "
        "--imports include "
        "--output {output}"
    )
    current_temp = TMP.joinpath("temp.txt")
    with open(current_temp, "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=current_temp.resolve().as_posix(),
        # term_file_filter=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
        output=Path(output).resolve().as_posix(),
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
# For this to work imports have to be manually removed from the Parking
# ontology. Something is going wrong with robot
chio_parking_viz = TMP.joinpath("chio_parking.owx")
if not chio_parking_viz.exists():
    terms = load_terms(FILEPATH.joinpath("chio_parking_viz.txt"))
    extract_subset(
        input=INPUT,
        output=chio_parking_viz,
        terms=terms,
    )
# %%
