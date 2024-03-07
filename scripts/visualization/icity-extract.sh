#!/bin/bash

tmpdir=tmp
mkdir -p ${tmpdir}

this_wd=scripts/visualization

icity_parking="https://enterpriseintegrationlab.github.io/icity/Parking/doc/ontology.ttl"

echo "downloading ${icity_parking}"
test -f ${tmpdir}/Parking.ttl && echo "${tmpdir}/Parking.ttl already exists." || curl -L -o ${tmpdir}/Parking.ttl ${icity_parking}

oldsec='
                                                  owl:imports <http://ontology.eil.utoronto.ca/icity/Building/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Change/1.1/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Contact/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Mereology/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/OM/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Organization/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Person/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/RecurringEvent/1.0/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/SpatialLoc/1.2/> ,
                                                              <http://ontology.eil.utoronto.ca/icity/Vehicle/1.2/> ;'

newsec=''

old_file_contents=$(< ${tmpdir}/Parking.ttl)
new_file_contents=${old_file_contents//"$oldsec"/"$newsec"}

printf '%s\n' "$new_file_contents" >${tmpdir}/parking_botched.ttl

java -jar robot.jar extract --input ${tmpdir}/parking_botched.ttl --method subset --term-file ${this_wd}/parking_space.txt --imports include --output ${tmpdir}/parking_space.ttl

java -jar robot.jar merge --input ${tmpdir}/parking_space.ttl convert --output ${tmpdir}/parking_space.owx --format owx
