#!/bin/bash

tmpdir=tmp
mkdir -p ${tmpdir}

this_wd=scripts/oeo-imports
ontology_name=chio
oeo_version="2.1.0"
ontology_source=src
imports="${ontology_source}/imports"

iri_base="http://openenergy-platform.org/ontology/"
oeo_base="http://openenergy-platform.org/ontology/oeo/releases/${oeo_version}"
oeo_new_iri="${ontology_name}/imports"
oeo_new_version_iri="${ontology_name}/dev/imports"

# Extractions from oeo-physical
echo "downloading ${oeo_base}/oeo-physical.omn"
test -f ${tmpdir}/oeo-physical.omn && echo "${tmpdir}/oeo-physical.omn already exists." || curl -L -o ${tmpdir}/oeo-physical.omn ${oeo_base}/oeo-physical.omn

echo "downloading ${oeo_base}/oeo-shared.omn"
test -f ${tmpdir}/oeo-shared.omn && echo "${tmpdir}/oeo-shared.omn already exists." || curl -L -o ${tmpdir}/oeo-shared.omn ${oeo_base}/oeo-shared.omn

echo "downloading ${oeo_base}/oeo-import-edits.owl"
test -f ${tmpdir}/oeo-import-edits.owl && echo "${tmpdir}/oeo-import-edits.owl already exists." || curl -L -o ${tmpdir}/oeo-import-edits.owl ${oeo_base}/oeo-import-edits.owl

echo "downloading ${oeo_base}/imports/ro-extracted.owl"
test -f ${tmpdir}/ro-extracted.owl && echo "${tmpdir}/ro-extracted.owl already exists." || curl -L -o ${tmpdir}/ro-extracted.owl ${oeo_base}/imports/ro-extracted.owl

echo "downloading ${oeo_base}/imports/uo-extracted.owl"
test -f ${tmpdir}/uo-extracted.owl && echo "${tmpdir}/uo-extracted.owl already exists." || curl -L -o ${tmpdir}/uo-extracted.owl ${oeo_base}/imports/uo-extracted.owl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/oeo-physical.omn --select imports extract --method subset --term-file ${this_wd}/oeo_vehicle.txt --imports exclude --output ${tmpdir}/oeo_vehicle.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/oeo-physical.omn --select imports extract --method subset --term-file ${this_wd}/oeo_grid.txt --imports exclude --output ${tmpdir}/oeo_grid.ttl

# Merging together

java -jar robot.jar merge --input ${tmpdir}/oeo_grid.ttl --input ${tmpdir}/oeo_vehicle.ttl annotate --annotation rdfs:comment "This is an extract of the Open Energy Ontology: https://github.com/OpenEnergyPlatform/ontology " --output ${imports}/oeo-extracted.ttl

java -jar robot.jar annotate --input ${imports}/oeo-extracted.ttl --ontology-iri ${iri_base}${oeo_new_iri}/oeo-extracted.ttl --version-iri ${iri_base}${oeo_new_version_iri}/oeo-extracted.ttl --output ${imports}/oeo-extracted.ttl

# Not necessary for imports but for the paper

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/oeo-physical.omn --select imports extract --method MIREOT  --imports exclude --branch-from-term http://openenergy-platform.org/ontology/oeo/OEO_00000146 --intermediates all --output ${tmpdir}/oeo_vehicle_ev_tax.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/oeo-physical.omn --select imports extract --method MIREOT  --imports exclude --branch-from-term http://openenergy-platform.org/ontology/oeo/OEO_00010273 --intermediates all --output ${tmpdir}/oeo_vehicle_lv_tax.ttl