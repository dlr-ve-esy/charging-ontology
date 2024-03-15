#!/bin/bash

tmpdir=tmp
mkdir -p ${tmpdir}

this_wd=scripts/cco-imports
ontology_name=chio
cco_version=master
ontology_source=src
imports="${ontology_source}/imports"

catalog_head='<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<catalog prefer="public" xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
    <group xml:base="">
    '
catalog_tail='    </group>
</catalog>'

iri_base="http://openenergy-platform.org/ontology/"
cco_base="https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/${cco_version}"
cco_new_iri="${ontology_name}/imports"
cco_new_version_iri="${ontology_name}/dev/imports"

# Extractions from Event Ontology
test -f ${tmpdir}/EventOntology.ttl && echo "${tmpdir}/EventOntology.ttl already exists." || curl -L -o ${tmpdir}/EventOntology.ttl ${cco_base}/EventOntology.ttl

# Extractions from Information EntityOntology
test -f ${tmpdir}/InformationEntityOntology.ttl && echo "${tmpdir}/InformationEntityOntology.ttl already exists." || curl -L -o ${tmpdir}/InformationEntityOntology.ttl ${cco_base}/InformationEntityOntology.ttl


# Extractions from Information EntityOntology
test -f ${tmpdir}/InformationEntityOntology.ttl && echo "${tmpdir}/InformationEntityOntology.ttl already exists." || curl -L -o ${tmpdir}/InformationEntityOntology.ttl ${cco_base}/InformationEntityOntology.ttl

# Extractions from Artifact Ontology
echo "downloading ${cco_base}/ArtifactOntology.ttl"
test -f ${tmpdir}/ArtifactOntology.ttl && echo "${tmpdir}/ArtifactOntology.ttl already exists." || curl -L -o ${tmpdir}/ArtifactOntology.ttl ${cco_base}/ArtifactOntology.ttl

# Extractions from ExtendedRelationOntology
echo "downloading ${cco_base}/ExtendedRelationOntology.ttl"
test -f ${tmpdir}/ExtendedRelationOntology.ttl && echo "${tmpdir}/ExtendedRelationOntology.ttl already exists." || curl -L -o ${tmpdir}/ExtendedRelationOntology.ttl ${cco_base}/ExtendedRelationOntology.ttl

# Extractions from Facility Ontology
echo "downloading ${cco_base}/FacilityOntology.ttl"
test -f ${tmpdir}/FacilityOntology.ttl && echo "${tmpdir}/FacilityOntology.ttl already exists." || curl -L -o ${tmpdir}/FacilityOntology.ttl ${cco_base}/FacilityOntology.ttl

# Extractions from GeospatialOntology Ontology
echo "downloading ${cco_base}/GeospatialOntology.ttl"
test -f ${tmpdir}/GeospatialOntology.ttl && echo "${tmpdir}/GeospatialOntology.ttl already exists." || curl -L -o ${tmpdir}/GeospatialOntology.ttl ${cco_base}/GeospatialOntology.ttl

# Extractions from AgentOntology Ontology
echo "downloading ${cco_base}/AgentOntology.ttl"
test -f ${tmpdir}/AgentOntology.ttl && echo "${tmpdir}/AgentOntology.ttl already exists." || curl -L -o ${tmpdir}/AgentOntology.ttl ${cco_base}/AgentOntology.ttl

# Extractions from TimeOntology Ontology
echo "downloading ${cco_base}/TimeOntology.ttl"
test -f ${tmpdir}/TimeOntology.ttl && echo "${tmpdir}/TimeOntology.ttl already exists." || curl -L -o ${tmpdir}/TimeOntology.ttl ${cco_base}/TimeOntology.ttl

# Extractions from InformationEntityOntology Ontology
echo "downloading ${cco_base}/InformationEntityOntology.ttl"
test -f ${tmpdir}/InformationEntityOntology.ttl && echo "${tmpdir}/InformationEntityOntology.ttl already exists." || curl -L -o ${tmpdir}/InformationEntityOntology.ttl ${cco_base}/InformationEntityOntology.ttl


java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/EventOntology.ttl --select imports extract --method MIREOT --upper-term "http://purl.obolibrary.org/obo/BFO_0000015" --lower-terms ${this_wd}/eo_stasis.txt --intermediates all --output ${tmpdir}/eo_stasis.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/EventOntology.ttl --select imports extract --method MIREOT --upper-term "http://purl.obolibrary.org/obo/BFO_0000015" --lower-term "http://www.ontologyrepository.com/CommonCoreOntologies/Change" --intermediates all --output ${tmpdir}/eo_change.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/EventOntology.ttl --select imports extract --method MIREOT --upper-term "http://purl.obolibrary.org/obo/BFO_0000144" --lower-term "http://www.ontologyrepository.com/CommonCoreOntologies/MaximumPower" --intermediates all --output ${tmpdir}/eo_process_profiles.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/ArtifactOntology.ttl --select imports extract --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000040 --lower-terms ${this_wd}/ao_artifacts.txt --intermediates all --output ${tmpdir}/ao_artifacts.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/ArtifactOntology.ttl --select imports extract --method subset --term-file ${this_wd}/ao_facility.txt --imports exclude --output ${tmpdir}/ao_facility.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/ArtifactOntology.ttl --select imports extract --method subset --term-file ${this_wd}/ao_infrastructure.txt --imports exclude --output ${tmpdir}/ao_infrastructure.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/ArtifactOntology.ttl --select imports extract --method MIREOT --upper-term http://www.ontologyrepository.com/CommonCoreOntologies/Artifact --lower-terms ${this_wd}/ao_vehicles.txt --intermediates all --output ${tmpdir}/ao_vehicles.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/FacilityOntology.ttl --select imports extract --method subset --term-file ${this_wd}/ao_facility_classes.txt --imports exclude --output ${tmpdir}/ao_facility_classes.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/GeospatialOntology.ttl --select imports extract  --method MIREOT --upper-term http://purl.obolibrary.org/obo/BFO_0000029 --lower-terms ${this_wd}/geo_base.txt --intermediates all --output ${tmpdir}/geo_base.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/AgentOntology.ttl --select imports extract --method MIREOT  --imports exclude --upper-term http://www.ontologyrepository.com/CommonCoreOntologies/GeospatialRegion --lower-terms ${this_wd}/geo_tree.txt --intermediates all --output ${tmpdir}/geo_tree.ttl

java -jar robot.jar remove --catalog ${tmpdir}/catalog.xml --input ${tmpdir}/InformationEntityOntology.ttl --select imports extract --method subset --term-file ${this_wd}/ieo_ops.txt --imports exclude --output ${tmpdir}/ieo_ops_base.ttl

java -jar robot.jar rename --input ${tmpdir}/ieo_ops_base.ttl --mappings ${this_wd}/ieo_ops_mappings.csv --allow-missing-entities true --output ${tmpdir}/ieo_ops.ttl

# Merging together

java -jar robot.jar merge --input ${tmpdir}/geo_tree.ttl --input ${tmpdir}/geo_base.ttl --input ${tmpdir}/ao_artifacts.ttl --input ${tmpdir}/ao_vehicles.ttl --input ${tmpdir}/ao_facility.ttl --input ${tmpdir}/ao_facility_classes.ttl --input ${tmpdir}/eo_stasis.ttl --input ${tmpdir}/eo_process_profiles.ttl --input ${tmpdir}/eo_change.ttl --input ${tmpdir}/ao_infrastructure.ttl --input ${tmpdir}/ieo_ops.ttl annotate --annotation rdfs:comment "This is an extract of the Common Core Ontologies: https://github.com/CommonCoreOntology/CommonCoreOntologies " --output src/imports/cco-extracted.ttl

java -jar robot.jar annotate --input ${imports}/cco-extracted.ttl --ontology-iri "${iri_base}${cco_new_iri}/cco-extracted.ttl" --version-iri "${iri_base}${cco_new_version_iri}/cco-extracted.ttl" --output ${imports}/cco-extracted.ttl