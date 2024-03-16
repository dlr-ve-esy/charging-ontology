#!/bin/bash

tmpdir=tmp
mkdir -p ${tmpdir}

this_wd=scripts/visualization
ontology_source=src
edits="${ontology_source}/edits"

java -jar robot.jar extract --input ${edits}/chio-core.ttl --method subset --term-file ${this_wd}/chio_parking_viz.txt --imports include --output ${tmpdir}/chio_parking.owx