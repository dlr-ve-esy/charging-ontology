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
echo "downloading ${oeo_base}/imports/iao-extracted.owl"
test -f ${tmpdir}/iao-extracted.owl && echo "${tmpdir}/iao-extracted.owl already exists." || curl -L -o ${tmpdir}/iao-extracted.owl ${oeo_base}/imports/iao-extracted.owl

java -jar robot.jar remove --input ${tmpdir}/iao-extracted.owl  --term http://purl.obolibrary.org/obo/IAO_0000013 --select "self" --exclude-term http://purl.obolibrary.org/obo/BFO_0000031 annotate --annotation http://purl.org/dc/terms/license http://creativecommons.org/licenses/by/4.0/ --output ${imports}/iao-extracted.ttl