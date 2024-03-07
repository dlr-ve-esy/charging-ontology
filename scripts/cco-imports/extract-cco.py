# %% [markdown]
# # Extraction of CCO modules
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
VERSION = "master"

ONTOLOGY_BASE = (
    "https://raw.githubusercontent.com/CommonCoreOntology/"
    "CommonCoreOntologies/{}/{}.ttl"
)
NEW_IRI = "{}/chio/imports/{}.ttl"
VERSION_IRI = "{}/chio/dev/imports/{}.ttl"

# Change these paths according to your setup.
ROBOT_PATH = BASEDIR.joinpath("robot.jar")
CCO = "tmp/MergedAllCoreOntology.ttl"
TARGET = BASEDIR.joinpath("src/imports/cco-extracted.ttl")
TMP = BASEDIR.joinpath("tmp")
TMP.mkdir(exist_ok=True)
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
    temporary_path = TMP.joinpath(f"{ONTOLOGY}.ttl")
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
    with open(TMP.joinpath("temp.txt"), "w") as fp:
        for term in lower_terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        lower_terms=TMP.joinpath("temp.txt").resolve().as_posix(),
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


def extract_star(input: str, output: str, terms: str):
    """Call robot to do a STAR extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method STAR "
        "--term-file {term_file} "
        "--imports exclude "
        "--output {output}"
    )
    with open(TMP.joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=TMP.joinpath("temp.txt").resolve().as_posix(),
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


def extract_tree(
    input: str,
    output: str,
    term: str,
):
    """Call robot to do a TOP extraction of a tree."""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method TOP "
        "--term {term} "
        "--imports exclude "
        "--output {output}"
    )
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term=term,
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


def extract_subset(input: str, output: str, terms: str):
    """Call robot to do a subset extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method subset "
        "--term-file {term_file} "
        "--imports include "
        # "filter --term-file {term_file_filter} "
        # "--select \"annotations self equivalents object-properties\" "
        "--output {output}"
    )
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=ROBOT_PATH.resolve().as_posix(),
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
# ## Extract classes from the event ontology
# %%
event_ontology = "EventOntology"
event_ontology = download_ontology_if_missing("EventOntology")
# %%
# Stasis
eo_stasis = TMP.joinpath("eo_stasis.ttl")
if not eo_stasis.exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000015"
    lower_terms = load_terms(FILEPATH.joinpath("eo_stasis.txt"))
    extract_mireot(
        input=event_ontology,
        output=eo_stasis,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Change
eo_change = TMP.joinpath("eo_change.ttl")
if not eo_change.exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000015"
    lower_terms = ["http://www.ontologyrepository.com/CommonCoreOntologies/Change"]
    extract_mireot(
        input=event_ontology,
        output=eo_change,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Process profiles
eo_process_profiles=TMP.joinpath("eo_process_profiles.ttl")
if not eo_process_profiles.exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000144"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/MaximumPower"
    ]
    extract_mireot(
        input=event_ontology,
        output=eo_process_profiles,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %% [markdown]
# ## Extract vehicle classes
# These axioms are very close to the ones from the OEO. I have to do some
# adjustments to ensure compatibility.
# Vehicle taxonomy from CCO
# Vehicle IRI from OEO and electric/ICE definitions from the OEO
# %%
artifact_ontology = download_ontology_if_missing("ArtifactOntology")
ao_artifacts = Path("tmp").joinpath("ao_artifacts.ttl")
if not ao_artifacts.exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000040"
    lower_terms = load_terms(FILEPATH.joinpath("ao_artifacts.txt"))
    extract_mireot(
        input=artifact_ontology,
        output=ao_artifacts,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Facility
ao_facility = TMP.joinpath("ao_facility.ttl")
if not ao_facility.exists():
    terms = load_terms(FILEPATH.joinpath("ao_facility.txt"))
    extract_subset(
        input=artifact_ontology,
        output=ao_facility,
        terms=terms,
    )
# %%
# Infrastructure
ao_infrastructure = TMP.joinpath("ao_infrastructure.ttl")
if not ao_infrastructure.exists():
    terms = load_terms(FILEPATH.joinpath("ao_infrastructure.txt"))
    extract_subset(
        input=artifact_ontology,
        output=ao_infrastructure,
        terms=terms,
    )
# %%
facility_ontology = download_ontology_if_missing("FacilityOntology")
ao_facility_classes = TMP.joinpath("ao_facility_classes.ttl")
if not ao_facility_classes.exists():
    terms = load_terms(FILEPATH.joinpath("ao_facility_classes.txt"))
    extract_subset(
        input=facility_ontology,
        output=ao_facility_classes,
        terms=terms,
    )
# %%
ao_vehicles = TMP.joinpath("ao_vehicles.ttl")
if not ao_vehicles.exists():
    upper_term = "http://www.ontologyrepository.com/CommonCoreOntologies/Artifact"
    lower_terms = load_terms(FILEPATH.joinpath("ao_vehicles.txt"))
    extract_mireot(
        input=artifact_ontology,
        output=ao_vehicles,
        upper_term=upper_term,
        lower_terms=lower_terms,
    )
# %%
# %%
geo_ontology = download_ontology_if_missing("GeospatialOntology")
geo_base = TMP.joinpath("geo_base.ttl")
if not geo_base.exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000029"
    lower_terms = load_terms(FILEPATH.joinpath("geo_base.txt"))
    extract_mireot(
        input=geo_ontology,
        output=geo_base,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
agent_ontology = download_ontology_if_missing("AgentOntology")
geo_tree = TMP.joinpath("geo_tree.ttl")
if not geo_tree.exists():
    upper_term = (
        "http://www.ontologyrepository.com/CommonCoreOntologies/GeospatialRegion"
    )
    lower_terms = load_terms(FILEPATH.joinpath("geo_tree.txt"))
    extract_mireot(
        input=agent_ontology,
        output=geo_tree,
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
input_string = ""
for element in [
    "geo_tree.ttl",
    "geo_base.ttl",
    "ao_artifacts.ttl",
    "ao_vehicles.ttl",
    "ao_facility.ttl",
    "ao_facility_classes.ttl",
    "eo_stasis.ttl",
    "eo_process_profiles.ttl",
    "eo_change.ttl",
    "ao_infrastructure.ttl",
]:
    input_string += f"--input {TMP.joinpath(element).resolve().as_posix()} "
# %%
if not TARGET.exists():
    merge_call = (
        "java -jar {jar} merge " + input_string + "annotate --annotation "
        'rdfs:comment "{annotation} " '
        "--output {output}"
    )
    annotation = (
        "This is an extract of the Common Core Ontologies: "
        "https://github.com/CommonCoreOntology/CommonCoreOntologies"
    )
    sp.call(
        merge_call.format(
            jar=ROBOT_PATH.resolve().as_posix(),
            annotation=annotation,
            output=TARGET.resolve().as_posix(),
        ),
        shell=True,
    )
    # Annotate with new iri
    annotate_call = "java -jar {jar} \
    annotate --input {input} \
    --ontology-iri {ontology_iri} \
    --version-iri {version_iri} \
    --output {output}"
    sp.call(
        annotate_call.format(
            jar=ROBOT_PATH.resolve().as_posix(),
            input=TARGET.resolve().as_posix(),
            ontology_iri=NEW_IRI.format(BASE_IRI, "cco-extracted"),
            version_iri=VERSION_IRI.format(BASE_IRI, "cco-extracted"),
            output=TARGET.resolve().as_posix(),
        ),
        shell=True,
    )
else:
    print(f"The file {TARGET} already exists, you are good to go.")
# %%
