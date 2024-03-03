# %% [markdown]
# # Extraction of CCO modules
# %%
import requests
import subprocess as sp
from pathlib import Path
import tempfile

BASE_IRI = "http://openenergy-platform.org/ontology"
VERSION = "master"

ONTOLOGY_BASE = (
    "https://raw.githubusercontent.com/CommonCoreOntology/"
    "CommonCoreOntologies/{}/{}.ttl"
)
NEW_IRI = "{}/chio/imports/{}.ttl"
VERSION_IRI = "{}/chio/dev/imports/{}.ttl"

# Change these paths according to your setup.
ROBOT_PATH = "../../robot.jar"
CCO = "tmp/MergedAllCoreOntology.ttl"
TARGET = "../../src/imports/cco-extracted.ttl"
Path("tmp").mkdir(exist_ok=True)
# %%


def download_ontology_if_missing(ONTOLOGY):
    """Helper function to download raw ontologies in a temporary folder.

    Args:
        ONTOLOGY (str): Name of the CCO module to be downloaded.
    """
    temporary_path = Path("tmp").joinpath(f"{ONTOLOGY}.ttl")
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
    """Call robot to do a STAR extraction"""
    extract_call = (
        "java -jar {jar} extract "
        "--input {input} "
        "--method STAR "
        "--term-file {term_file} "
        "--imports exclude "
        "--output {output}"
    )
    with open(Path("tmp").joinpath("temp.txt"), "w") as fp:
        for term in terms:
            fp.write(term + "\n")
    debug_string = extract_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(input).resolve().as_posix(),
        term_file=Path("tmp").joinpath("temp.txt").resolve().as_posix(),
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
        jar=Path(ROBOT_PATH).resolve().as_posix(),
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
# ## Extract classes from the event ontology
# %%
event_ontology = "EventOntology"
event_ontology = download_ontology_if_missing("EventOntology")
# %%
# Stasis
if not Path("tmp").joinpath("eo_stasis.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000015"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/StableOrientation",
        "http://www.ontologyrepository.com/CommonCoreOntologies/StasisOfDisposition",
        "http://www.ontologyrepository.com/CommonCoreOntologies/StasisOfFunction",
        "http://www.ontologyrepository.com/CommonCoreOntologies/StasisOfRole",
        "http://www.ontologyrepository.com/CommonCoreOntologies/ActiveStasis"
    ]
    extract_mireot(
        input=event_ontology,
        output=Path("tmp").joinpath("eo_stasis.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Change
if not Path("tmp").joinpath("eo_change.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000015"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/Change"
    ]
    extract_mireot(
        input=event_ontology,
        output=Path("tmp").joinpath("eo_change.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Process profiles
if not Path("tmp").joinpath("eo_process_profiles.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000144"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/MaximumPower"
    ]
    extract_mireot(
        input=event_ontology,
        output=Path("tmp").joinpath("eo_process_profiles.ttl"),
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
if not Path("tmp").joinpath("ao_artifacts.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000040"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/ElectricMotor",
        "http://www.ontologyrepository.com/CommonCoreOntologies/CompressionIgnitionEngine",
        "http://www.ontologyrepository.com/CommonCoreOntologies/SparkIgnitionEngine",
    ]
    extract_mireot(
        input=artifact_ontology,
        output=Path("tmp").joinpath("ao_artifacts.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
# Facility
if not Path("tmp").joinpath("ao_facitlity.ttl").exists():
    terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/TransportationFacilitys",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Artifact",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Facility",
        "http://www.ontologyrepository.com/CommonCoreOntologies/PortionOfGeosphere",
        "http://purl.obolibrary.org/obo/BFO_0000171",
        "http://purl.obolibrary.org/obo/BFO_0000023",
        "http://purl.obolibrary.org/obo/BFO_0000024"
        "http://www.ontologyrepository.com/CommonCoreOntologies/InfrastructureRole",
        "http://www.ontologyrepository.com/CommonCoreOntologies/InfrastructureElement",
        "http://purl.obolibrary.org/obo/BFO_0000040",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Infrastructure",
        "http://www.ontologyrepository.com/CommonCoreOntologies/TransportationInfrastructure",
        "http://purl.obolibrary.org/obo/BFO_0000196"

    ]
    extract_subset(
        input=artifact_ontology,
        output=Path("tmp").joinpath("ao_facitlity.ttl"),
        terms=terms
    )
# %%
if not Path("tmp").joinpath("ao_vehicles.ttl").exists():
    upper_term = "http://www.ontologyrepository.com/CommonCoreOntologies/Artifact"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/Truck",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Motorcycle",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Bus",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Automobile",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Bicycle"
    ]
    extract_mireot(
        input=artifact_ontology,
        output=Path("tmp").joinpath("ao_vehicles.ttl"),
        upper_term=upper_term,
        lower_terms=lower_terms
    )
# %%
# %%
artifact_ontology = download_ontology_if_missing("ArtifactOntology")
if not Path("tmp").joinpath("ao_artifacts.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000040"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/ElectricMotor",
        "http://www.ontologyrepository.com/CommonCoreOntologies/CompressionIgnitionEngine",
        "http://www.ontologyrepository.com/CommonCoreOntologies/SparkIgnitionEngine",
    ]
    extract_mireot(
        input=artifact_ontology,
        output=Path("tmp").joinpath("ao_artifacts.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
geo_ontology = download_ontology_if_missing("GeospatialOntology")
if not Path("tmp").joinpath("geo_base.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000029"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/Continent",
        "http://www.ontologyrepository.com/CommonCoreOntologies/GeospatialLocation",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Subcontinent",
    ]
    extract_mireot(
        input=geo_ontology,
        output=Path("tmp").joinpath("geo_base.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
agent_ontology = download_ontology_if_missing("AgentOntology")
if not Path("tmp").joinpath("geo_tree.ttl").exists():
    upper_term = "http://www.ontologyrepository.com/CommonCoreOntologies/GeospatialRegion"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/County",
        "http://www.ontologyrepository.com/CommonCoreOntologies/State",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Province",
        "http://www.ontologyrepository.com/CommonCoreOntologies/FourthOrderAdministrativeRegion",
        "http://www.ontologyrepository.com/CommonCoreOntologies/City",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Town",
        "http://www.ontologyrepository.com/CommonCoreOntologies/Village",
        "http://www.ontologyrepository.com/CommonCoreOntologies/SecondOrderAdministrativeRegion",
        "http://www.ontologyrepository.com/CommonCoreOntologies/ThirdOrderAdministrativeRegion"
    ]
    extract_mireot(
        input=agent_ontology,
        output=Path("tmp").joinpath("geo_tree.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
input_string =""
for element in ["geo_tree.ttl", "geo_base.ttl", "ao_artifacts.ttl",
                "ao_vehicles.ttl","ao_facitlity.ttl", "eo_stasis.ttl",
                "eo_process_profiles.ttl", "eo_change.ttl"]:
    input_string += f"--input tmp/{element} "
# %%
if not Path(TARGET).exists():
    merge_call = ("java -jar {jar} merge " +  input_string +
                     "annotate --annotation "
                     "rdfs:comment \"{annotation} \" "
                     "--output {output}" )
    annotation = (
        "This is an extract of the Common Core Ontologies: "
        "https://github.com/CommonCoreOntology/CommonCoreOntologies"
    )
    sp.call(
        merge_call.format(
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            annotation=annotation,
            output=Path(TARGET).resolve().as_posix(),
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
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            input=Path(TARGET).resolve().as_posix(),
            ontology_iri=NEW_IRI.format(BASE_IRI, "cco-extracted"),
            version_iri=VERSION_IRI.format(BASE_IRI, "cco-extracted"),
            output=Path(TARGET).resolve().as_posix(),
        ),
        shell=True,
    )
else:
    print(f"The file {TARGET} already exists, you are good to go.")
# %%