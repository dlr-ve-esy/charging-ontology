#!/bin/bash

tmpdir=tmp
mkdir -p ${tmpdir}

ontology_name=chio
cco_version=master
ontology_source=src
imports="${ontology_source}/imports"

iri_base="http://openenergy-platform.org/ontology/"
cco_base="https://raw.githubusercontent.com/CommonCoreOntology/${cco_version}"
cco_new_iri="${ontology_name}/imports"
cco_new_version_iri="${ontology_name}/dev/imports"

# Extractions from Event Ontology
test -f $filename && echo "${tmpdir}/EventOntology.ttl already exists." || curl -L -o ${tmpdir}/EventOntology.ttl ${cco_base}/${cco_version}/EventOntology.ttl

java -jar robot.jar extract --input ${tmpdir}/EventOntology.ttl --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000015 --lower-terms scripts/cco-imports/eo_stasis.txt --intermediates all --output ${tmpdir}/eo_stasis.ttl

java -jar robot.jar extract --input ${tmpdir}/EventOntology.ttl --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000015 --lower-term http://www.ontologyrepository.com/CommonCoreOntologies/Change --intermediates all --output ${tmpdir}/eo_change.ttl

java -jar robot.jar extract --input ${tmpdir}/EventOntology.ttl --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000144 --lower-term http://www.ontologyrepository.com/CommonCoreOntologies/MaximumPower --intermediates all --output ${tmpdir}/eo_process_profiles.ttl

# Extractions from Artifact Ontology
test -f $filename && echo "${tmpdir}/ArtifactOntology.ttl already exists." || curl -L -o ${tmpdir}/ArtifactOntology.ttl ${cco_base}/${cco_version}/ArtifactOntology.ttl

java -jar robot.jar extract --input ${tmpdir}/ArtifactOntology.ttl --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000040 --lower-terms scripts/cco-imports/ao_artifacts.txt --intermediates all --output ${tmpdir}/ao_artifacts.ttl

java -jar robot.jar extract --input ${tmpdir}/ArtifactOntology.ttl --method subset --term-file scripts/cco-imports/ao_facility.txt --imports include --output ${tmpdir}/ao_facility.ttl

java -jar robot.jar extract --input ${tmpdir}/ArtifactOntology.ttl --method subset --term-file scripts/cco-imports/ao_infrastructure.txt --imports include --output ${tmpdir}/ao_infrastructure.ttl

java -jar robot.jar extract --input ${tmpdir}/ArtifactOntology.ttl --method MIREOT --upper-term http://www.ontologyrepository.com/CommonCoreOntologies/Artifact --lower-terms scripts/cco-imports/ao_vehicles.txt --intermediates all --output ${tmpdir}/ao_vehicles.ttl

# Extractions from Facility Ontology
test -f $filename && echo "${tmpdir}/FacilityOntology.ttl already exists." || curl -L -o ${tmpdir}/FacilityOntology.ttl ${cco_base}/${cco_version}/FacilityOntology.ttl

java -jar robot.jar extract --input ${tmpdir}/FacilityOntology.ttl --method subset --term-file scripts/cco-imports/ao_facility_classes.txt --imports include --output ${tmpdir}/ao_facility_classes.ttl

# Extractions from GeospatialOntology Ontology
test -f $filename && echo "${tmpdir}/GeospatialOntology.ttl already exists." || curl -L -o ${tmpdir}/GeospatialOntology.ttl ${cco_base}/${cco_version}/GeospatialOntology.ttl

java -jar robot.jar extract --input ${tmpdir}/GeospatialOntology.ttl --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000029 --lower-terms scripts/cco-imports/geo_base.txt --intermediates all --output ${tmpdir}/geo_base.ttl

# Extractions from AgentOntology Ontology
test -f $filename && echo "${tmpdir}/AgentOntology.ttl already exists." || curl -L -o ${tmpdir}/AgentOntology.ttl ${cco_base}/${cco_version}/AgentOntology.ttl

java -jar robot.jar extract --input ${tmpdir}/AgentOntology.ttl --method MIREOT --upper-term http://www.ontologyrepository.com/CommonCoreOntologies/GeospatialRegion --lower-terms scripts/cco-imports/geo_tree.txt --intermediates all --output ${tmpdir}/geo_tree.ttl

# Merging together

java -jar robot.jar merge --input ${tmpdir}/geo_tree.ttl --input ${tmpdir}/geo_base.ttl --input ${tmpdir}/ao_artifacts.ttl --input ${tmpdir}/ao_vehicles.ttl --input ${tmpdir}/ao_facility.ttl --input ${tmpdir}/ao_facility_classes.ttl --input ${tmpdir}/eo_stasis.ttl --input ${tmpdir}/eo_process_profiles.ttl --input ${tmpdir}/eo_change.ttl --input ${tmpdir}/ao_infrastructure.ttl annotate --annotation rdfs:comment "This is an extract of the Common Core Ontologies: https://github.com/CommonCoreOntology/CommonCoreOntologies " --output src/imports/cco-extracted.ttl

java -jar robot.jar annotate --input /scratch/ws/m5/arel_eu-onto-dev/charging-ontology/src/imports/cco-extracted.ttl --ontology-iri "${iri_base}${cco_new_iri}/cco-extracted.ttl" --version-iri "${iri_base}${cco_new_version_iri}/cco-extracted.ttl" --output ${imports}/cco-extracted.ttl