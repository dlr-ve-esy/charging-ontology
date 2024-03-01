# %%
import requests
import subprocess as sp
from pathlib import Path

# NOTE: Versioning in CCO is confusing, is very tricky to import the latest
# released version, that is why we have to bind it to a commit

BASE_IRI = "http://openenergy-platform.org/ontology"
COMMIT = "a99731c59859047e84253d15f8eba438b0aa71da"
NAME = "MergedAllCoreOntology-v1.5-2024-02-14.ttl"
ONTOLOGY_BASE = (
    "https://raw.githubusercontent.com/CommonCoreOntology/"
    f"CommonCoreOntologies/{COMMIT}/cco-merged/{NAME}"
)
UPPER_TERM = "http://purl.obolibrary.org/obo/BFO_0000003"
CLASS_IRI = "http://purl.obolibrary.org/obo/BFO_0000144"
NEW_IRI = f"{BASE_IRI}/chio/imports/cco-extracted.ttl"
VERSION_IRI = f"{BASE_IRI}/chio/dev/imports/cco-extracted.ttl"
TERM_FILE = "cco-w-hierarchy.txt"
# Change these paths according to your setup.
ROBOT_PATH = "../../robot.jar"
CCO = "tmp/MergedAllCoreOntology.ttl"
TARGET = "../../src/imports/cco-extracted.ttl"
Path("tmp").mkdir(exist_ok=True)
# %%
if not Path(CCO).exists():
    with open(CCO, "wb") as local:
        response = requests.get(ONTOLOGY_BASE)
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {CCO} already exists, you are good to go.")
# %%
if not Path(TARGET).exists():
    extract_call = 'java -jar {jar} \
merge --input {input} extract \
--method {method} \
--lower-terms {term_file} \
--intermediates all \
--upper-term owl:Class \
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
