#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2024 German Aerospace Center (DLR)
# SPDX-License-Identifier: BSD-3-Clause
tmpdir=tmp
mkdir -p ${tmpdir}

this_wd=scripts/visualization
ontology_source=src
imports="${ontology_source}/imports"

java -jar robot.jar merge --input ${tmpdir}/ao_infrastructure.ttl convert --output ${tmpdir}/ao_infrastructure.owx --format owx

java -jar robot.jar merge --input ${imports}/bfo-core.ttl convert --output ${tmpdir}/bfo.owx --format owx

java -jar robot.jar merge --input ${tmpdir}/oeo_vehicle.ttl convert --output ${tmpdir}/oeo_vehicle.owx --format owx

java -jar robot.jar merge --input ${tmpdir}/ao_vehicles.ttl convert --output ${tmpdir}/ao_vehicles.owx --format owx

java -jar robot.jar merge --input ${tmpdir}/oeo_vehicle_ev_tax.ttl convert --output ${tmpdir}/oeo_vehicle_ev_tax.owx --format owx

java -jar robot.jar merge --input ${tmpdir}/oeo_vehicle_lv_tax.ttl convert --output ${tmpdir}/oeo_vehicle_lv_tax.owx --format owx