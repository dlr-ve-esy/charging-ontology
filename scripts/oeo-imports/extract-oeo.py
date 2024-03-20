# SPDX-FileCopyrightText: Copyright (c) 2024 German Aerospace Center (DLR)
# SPDX-License-Identifier: BSD-3-Clause
# %%
import requests
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

BASE_IRI = "http://openenergy-platform.org/ontology"
VERSION = "2.1.0"
ONTOLOGY_BASE = "http://openenergy-platform.org/ontology/oeo/releases/{}/{}"
# Change these paths according to your setup.
ROBOT_PATH = BASEDIR.joinpath("robot.jar")
IAO = BASEDIR.joinpath("src/imports/iao-extracted.ttl")

TMP = BASEDIR.joinpath("tmp")
TMP.mkdir(exist_ok=True)

NEW_IRI = "{}/chio/imports/{}.ttl"
VERSION_IRI = "{}/chio/dev/imports/{}.ttl"

TARGET = BASEDIR.joinpath("src/imports/oeo-extracted.ttl")


# %%
def load_terms(term_file):
    with open(term_file, "r") as terms:
        term_list = [l for l in terms.readlines()]
    return term_list


def download_ontology_if_missing(ONTOLOGY):
    """Helper function to download raw ontologies in a temporary folder.

    Args:
        ONTOLOGY (str): Name of the CCO module to be downloaded.
    """
    temporary_path = TMP.joinpath(f"{ONTOLOGY}")
    TMP.joinpath(f"{ONTOLOGY}").parent.mkdir(exist_ok=True)
    if not temporary_path.exists():
        with open(temporary_path, "wb") as local:
            response = requests.get(ONTOLOGY_BASE.format(VERSION, ONTOLOGY))
            if response.status_code == 200:
                local.write(response.content)
    else:
        print(f"The file {temporary_path} already exists, you are good to go.")
    return temporary_path


# %%
def extract_mireot_tree(
    input: str,
    output: str,
    branch: str,
    intermediates="all",
    upper_term: str = "owl:Thing",
):
    """Call robot to do a MIREOT extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method MIREOT "
        "--branch-from-term {branch} "
        "--intermediates {intermediates} "
        "--output {output}"
    )
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        branch=branch,
        intermediates=intermediates,
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
def extract_star(input: str, output: str, terms: str):
    """Call robot to do a subset extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method STAR "
        "--term-file {term_file} "
        "--imports exclude "
        # "filter --term-file {term_file_filter} "
        # "--select \"annotations self equivalents object-properties\" "
        "--output {output}"
    )
    with open(TMP.joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=TMP.joinpath("temp.txt").resolve().as_posix(),
        # term_file_filter=TMP.joinpath("temp.txt").resolve().as_posix(),
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


def extract_subset(input: str, output: str, terms: str):
    """Call robot to do a subset extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method subset "
        "--term-file {term_file} "
        "--imports exclude "
        # "filter --term-file {term_file_filter} "
        # "--select \"annotations self equivalents object-properties\" "
        "--output {output}"
    )
    with open(TMP.joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=TMP.joinpath("temp.txt").resolve().as_posix(),
        # term_file_filter=TMP.joinpath("temp.txt").resolve().as_posix(),
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


# %% [markdown]
## OEO Vehicle axioms
# The main axioms of electric vehicle are extracted from OEO, whereas the
# vehicle taxonomy comes from the CCO.
# %%
oeo_physical = download_ontology_if_missing("imports/oeo-physical.omn")
oeo_vehicle = TMP.joinpath("oeo_vehicle.ttl")
terms = load_terms(FILEPATH.joinpath("oeo_vehicle.txt"))
code = extract_subset(oeo_physical, oeo_vehicle, terms=terms)
# %% [markdown]
## OEO grid axioms
# %%
oeo_grid = TMP.joinpath("oeo_grid.ttl")
terms = load_terms(FILEPATH.joinpath("oeo_grid.txt"))
code = extract_subset(oeo_physical, oeo_grid, terms=terms)
# %%
input_string = ""
for element in ["oeo_grid.ttl", "oeo_vehicle.ttl"]:
    input_string += f"--input {TMP.joinpath(element).as_posix()} "
# %%
if not TARGET.exists():
    merge_call = (
        "java -jar {jar} merge " + input_string + "annotate --annotation "
        'rdfs:comment "{annotation} " '
        "--output {output}"
    )
    annotation = (
        "This is an extract of the Open Energy Ontology: "
        "https://github.com/OpenEnergyPlatform/ontology"
    )
    sp.call(
        merge_call.format(
            jar=ROBOT_PATH.resolve().as_posix(),
            annotation=annotation,
            output=TARGET.resolve().as_posix(),
        ),
        shell=True,
    )
    # Annotate with new iri, OEO has a public domain license.
    annotate_call = "java -jar {jar} \
    annotate --input {input} \
    --ontology-iri {ontology_iri} \
    --version-iri {version_iri} \
    --annotation http://purl.org/dc/terms/license http://creativecommons.org/publicdomain/zero/1.0/ \
    --output {output}"
    sp.call(
        annotate_call.format(
            jar=ROBOT_PATH.resolve().as_posix(),
            input=TARGET.resolve().as_posix(),
            ontology_iri=NEW_IRI.format(BASE_IRI, "oeo-extracted"),
            version_iri=VERSION_IRI.format(BASE_IRI, "oeo-extracted"),
            output=TARGET.resolve().as_posix(),
        ),
        shell=True,
    )
else:
    print(f"The file {TARGET} already exists, you are good to go.")
# %%
# %%
# Get IAO imports
iao_temp = TMP.joinpath("iao-extracted.owl")
if not iao_temp.exists():
    with open(iao_temp, "wb") as local:
        response = requests.get(
            ONTOLOGY_BASE.format(VERSION, "imports/iao-extracted.owl")
        )
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {iao_temp} already exists, you are good to go.")

# %%
IAO_DROPPED = BASEDIR.joinpath("scripts/oeo-imports/iao-dropped.txt")
if iao_temp.exists():
    extract_call = 'java -jar {jar} \
remove --input {input}  \
--term-file {term_file} \
--select "self" \
--exclude-term http://purl.obolibrary.org/obo/BFO_0000031 \
annotate --annotation http://purl.org/dc/terms/license http://creativecommons.org/licenses/by/4.0/ \
--output {output}'

    sp.call(
        extract_call.format(
            jar=ROBOT_PATH.resolve().as_posix(),
            input=iao_temp.resolve().as_posix(),
            term_file=IAO_DROPPED,
            output=IAO.resolve().as_posix(),
        ),
        shell=True,
    )
# %%
## OEO Vehicle taxonomy (for paper)
# %%
oeo_vehicle_ev_tax = TMP.joinpath("oeo_vehicle_ev_tax.ttl")
if not oeo_vehicle_ev_tax.exists():
    parent = "http://openenergy-platform.org/ontology/oeo/OEO_00000146"
    extract_mireot_tree(
        input=oeo_physical,
        output=oeo_vehicle_ev_tax,
        branch=parent,
    )
oeo_vehicle_lv_tax = TMP.joinpath("oeo_vehicle_lv_tax.ttl")
if not oeo_vehicle_lv_tax.exists():
    parent = "http://openenergy-platform.org/ontology/oeo/OEO_00010273"
    extract_mireot_tree(
        input=oeo_physical,
        output=oeo_vehicle_lv_tax,
        branch=parent,
    )
# %%
