# SPDX-FileCopyrightText: Copyright (c) 2024 German Aerospace Center (DLR)
# SPDX-License-Identifier: BSD-3-Clause
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

TARGET = TMP.joinpath("Parking.ttl")
# %%
if not TARGET.exists():
    with open(TARGET, "wb") as local:
        response = requests.get(ONTOLOGY_BASE)
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {TARGET} already exists, you are good to go.")


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
# Ugly fix, not even ROBOT can open the file
botched_parking_ontology = TMP.joinpath("parking_botched.ttl")
if TARGET.exists():
    IMPORT_BLOCK = """ <http://ontology.eil.utoronto.ca/icity/Building/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Change/1.1/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Contact/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Mereology/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/OM/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Organization/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Person/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/RecurringEvent/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/SpatialLoc/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Vehicle/1.2/> ;"""
    REDUCED_BLOCK ="""<http://ontology.eil.utoronto.ca/icity/Change/1.1/> ;"""
    with open(TARGET, "r") as original:
        text = original.read()
        new_text = text.replace(IMPORT_BLOCK, REDUCED_BLOCK)

    with open(botched_parking_ontology, "w", encoding="utf-8") as new:
        new.write(new_text)
        
# %%
# For this to work imports have to be manually removed from the Parking
# ontology. Something is going wrong with robot
parking_space = TMP.joinpath("parking_space.ttl")
if not parking_space.exists():
    terms = load_terms(FILEPATH.joinpath("parking_space.txt"))
    extract_subset(
        input=botched_parking_ontology,
        output=parking_space,
        terms=terms,
    )
robot_convert(TMP.joinpath("parking_space.ttl"), TMP.joinpath("parking_space.owx"))
# %%
