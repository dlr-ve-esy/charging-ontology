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
UPPER_TERM = "http://purl.obolibrary.org/obo/BFO_0000003"
CLASS_IRI = "http://purl.obolibrary.org/obo/BFO_0000144"
NEW_IRI = "{}/chio/imports/{}.ttl"
VERSION_IRI = "{}/chio/dev/imports/{}.ttl"
TERM_FILE = "cco-w-hierarchy.txt"

# Change these paths according to your setup.
ROBOT_PATH = "../../robot.jar"
CCO = "tmp/MergedAllCoreOntology.ttl"
TARGET = "../../src/imports/cco-extracted.ttl"
Path("tmp").mkdir(exist_ok=True)
# %%


def download_ontology_if_missing(ONTOLOGY):
    """Helper function to download raw ontologies in a temporary folder.

    Args:
        ONTOLOGY (_type_): _description_
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
def extract_mierot(
    input: str,
    output: str,
    lower_terms: str,
    intermediates="all",
    upper_term: str = "owl:Thing",
):
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
    ]
    extract_mierot(
        input=event_ontology,
        output=Path("tmp").joinpath("eo_stasis.ttl"),
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
    extract_mierot(
        input=event_ontology,
        output=Path("tmp").joinpath("eo_process_profiles.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %% [markdown]
# ## Exrract vehicle classes
# These axioms are very close to the ones from the OEO. I have to do some
# adjustments to ensure compatibility.
# Vehicle taxonomy from CCO
# Vehicle IRI from OEO and electric/ICE definitions from the OEO
# %%
artifact_ontology = download_ontology_if_missing("ArtifactOntology")
if not Path("tmp").joinpath("eo_artifacts.ttl").exists():
    upper_term = "http://purl.obolibrary.org/obo/BFO_0000040"
    lower_terms = [
        "http://www.ontologyrepository.com/CommonCoreOntologies/ElectricMotor",
        "http://www.ontologyrepository.com/CommonCoreOntologies/CompressionIgnitionEngine",
        "http://www.ontologyrepository.com/CommonCoreOntologies/SparkIgnitionEngine",
    ]
    extract_mierot(
        input=artifact_ontology,
        output=Path("tmp").joinpath("eo_artifacts.ttl"),
        lower_terms=lower_terms,
        upper_term=upper_term,
    )
# %%
if not Path(TARGET).exists():
    extract_call = 'java -jar {jar} \
merge --input {input} extract \
--method {method} \
--lower-terms {term_file} \
--intermediates all \
annotate --annotation rdfs:comment "{annotation}" \
--output {output}'

    annotation = (
        "These axioms were extracted from the common core ontology:"
        " https://github.com/CommonCoreOntology/CommonCoreOntologies"
    )
    sp.call(
        extract_call.format(
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            input=Path(CCO).resolve().as_posix(),
            method="MIREOT",
            term_file=TERM_FILE,
            upper_term=UPPER_TERM,
            annotation=annotation,
            output=Path(TARGET).resolve().as_posix(),
        ),
        shell=True,
    )
else:
    print(f"The file {TARGET} already exists, you are good to go.")

# %% [markdown]
# A bunch of renames.
# %%
if Path(TARGET).exists():
    rename_call = "java -jar {jar} \
rename --input {input} \
--mappings {mappings} \
--output {output}"

    sp.call(
        rename_call.format(
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            input=Path(TARGET).resolve().as_posix(),
            mappings=Path("definition-mapping.tsv").resolve().as_posix(),
            output=Path(TARGET).resolve().as_posix(),
        ),
        shell=True,
    )
# %%
rename_mappings_call = "java -jar {jar} \
rename --input {input} \
--prefix-mappings {prefix_map} \
--allow-missing-entities true \
--output {output}"
sp.call(
    rename_mappings_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(TARGET).resolve().as_posix(),
        prefix_map=Path("prefix-mappings.tsv").resolve().as_posix(),
        output=Path(TARGET).resolve().as_posix(),
    ),
    shell=True,
)
# %%
annotate_call = "java -jar {jar} \
annotate --input {input} \
--ontology-iri {ontology_iri} \
--version-iri {version_iri} \
--output {output}"
sp.call(
    annotate_call.format(
        jar=Path(ROBOT_PATH).resolve().as_posix(),
        input=Path(TARGET).resolve().as_posix(),
        ontology_iri=NEW_IRI,
        version_iri=VERSION_IRI,
        output=Path(TARGET).resolve().as_posix(),
    ),
    shell=True,
)
# %%
