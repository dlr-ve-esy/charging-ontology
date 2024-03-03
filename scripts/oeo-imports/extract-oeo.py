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


def download_ontology_if_missing(ONTOLOGY):
    """Helper function to download raw ontologies in a temporary folder.

    Args:
        ONTOLOGY (str): Name of the CCO module to be downloaded.
    """
    temporary_path = Path("tmp").joinpath(f"{ONTOLOGY}")
    Path("tmp").joinpath(f"{ONTOLOGY}").parent.mkdir(exist_ok=True)
    if not Path(temporary_path).exists():
        with open(temporary_path, "wb") as local:
            response = requests.get(ONTOLOGY_BASE.format(VERSION, ONTOLOGY))
            if response.status_code == 200:
                local.write(response.content)
    else:
        print(f"The file {temporary_path} already exists, you are good to go.")
    return temporary_path


# %%
def extract_mireot(
    input: str,
    output: str,
    lower_terms: str,
    intermediates="all",
    upper_term: str = "owl:Thing",
):
    """Call robot to do a MIREOT extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method MIREOT "
        "--upper-term {upper_term} "
        "--lower-terms {lower_terms} "
        "--intermediates {intermediates} "
        "--output {output}"
    )
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in lower_terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        lower_terms=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
        upper_term=upper_term,
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
def extract_star(
    input: str,
    output: str,
    terms: str
):
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
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
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

def extract_subset(
    input: str,
    output: str,
    terms: str
):
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
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
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
# %% [markdown]
## OEO Vehicle axioms
# The main axioms of electric vehicle are extracted from OEO, whereas the 
# vehicle taxonomy comes from the CCO.
# %%
oeo_physical = download_ontology_if_missing("imports/oeo-physical.omn")
terms = ["http://openenergy-platform.org/ontology/oeo/OEO_00010024",
         "http://purl.obolibrary.org/obo/BFO_0000051",
         "http://openenergy-platform.org/ontology/oeo/OEO_00010026",
         "http://openenergy-platform.org/ontology/oeo/OEO_00000146",
         "http://openenergy-platform.org/ontology/oeo/OEO_00010028",
         "http://openenergy-platform.org/ontology/oeo/OEO_00010027",
         "http://openenergy-platform.org/ontology/oeo/OEO_00000068",
         "http://openenergy-platform.org/ontology/oeo/OEO_00010026"]
code =extract_subset(oeo_physical,"tmp/oeo_vehicle.ttl",terms=terms)
# %% [markdown]
## OEO grid axioms
# %%
terms = ["http://openenergy-platform.org/ontology/oeo/OEO_00320065",
         "http://openenergy-platform.org/ontology/oeo/OEO_00320040",
         "http://openenergy-platform.org/ontology/oeo/OEO_00000144",
         "http://openenergy-platform.org/ontology/oeo/OEO_00020006",
         "http://openenergy-platform.org/ontology/oeo/OEO_00000200",
         "http://openenergy-platform.org/ontology/oeo/OEO_00000143",
         "http://purl.obolibrary.org/obo/BFO_0000051",
         "http://purl.obolibrary.org/obo/BFO_0000027",
         "http://openenergy-platform.org/ontology/oeo/OEO_00320064"]
code =extract_subset(oeo_physical,"tmp/oeo_grid.ttl",terms=terms)
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
