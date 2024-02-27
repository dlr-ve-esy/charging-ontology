# %%
import requests
import subprocess as sp
from pathlib import Path

CCO_COMMIT = "a9e8c72eda3e01acbfca3eaaa837b7385d853c8a"
ONTOLOGY_BASE = "https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/{}/EventOntology.ttl"
UPPER_TERM = "http://purl.obolibrary.org/obo/BFO_0000015"
CLASS_IRI = "http://purl.obolibrary.org/obo/BFO_0000144"

# Change these paths according to your setup.
ROBOT_PATH = "../robot.jar"
EVENT_ONTOLOGY = "tmp/EventOntology.ttl"
TARGET = "../src/imports/process-profile.ttl"
Path("tmp").mkdir(exist_ok=True)
# %%
if not Path(EVENT_ONTOLOGY).exists():
    with open(EVENT_ONTOLOGY, "wb") as local:
        response = requests.get(ONTOLOGY_BASE.format(CCO_COMMIT))
        if response.status_code == 200:
            local.write(response.content)
else:
    print(f"The file {EVENT_ONTOLOGY} already exists, you are good to go.")
# %%
if not Path(TARGET).exists():
    extract_call = 'java -jar {jar} \
extract --input {input} \
--method {method} \
--lower-term {lower_term} \
--intermediates none \
--upper-term {upper_term} \
annotate --annotation rdfs:comment "{annotation}" \
--output {output}'

    annotation = "This class was extracted from the EventOntology because the newest BFO does not have it. Extracted from: https://github.com/CommonCoreOntology/CommonCoreOntologies"
    sp.call(
        extract_call.format(
            jar=Path(ROBOT_PATH).resolve().as_posix(),
            input=Path(EVENT_ONTOLOGY).resolve().as_posix(),
            method="MIREOT",
            lower_term=CLASS_IRI,
            upper_term=UPPER_TERM,
            annotation=annotation,
            output=Path(TARGET).resolve().as_posix(),
        ),
        shell=True,
    )
else:
    print(f"The file {TARGET} already exists, you are good to go.")
# %%
