ONTOLOGY_NAME := chio
MKDIR_P = mkdir -p
VERSION:= $(shell cat VERSION)
VERSIONDIR := build/chio/$(VERSION)
ONTOLOGY_SOURCE := src
BFOCOMMIT := d9aa636303766bfb6a7a6d46265873f96cdd8584
TMP := tmp
IMPORTS := $(ONTOLOGY_SOURCE)/imports

subst_paths =	${subst $(ONTOLOGY_SOURCE),$(VERSIONDIR),${patsubst $(ONTOLOGY_SOURCE)/edits/%,$(ONTOLOGY_SOURCE)/modules/%,$(1)}}
subst_paths_owl =	${subst $(VERSIONDIR),$(VERSIONDIR)/owl,${patsubst %.ttl,%.owl,$(1)}}

OWL_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)/* -type f -name "*.owl"))
OMN_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)/* -type f -name "*.omn"))
TTL_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)* -type f -name "*.ttl"))

IRI_BASE := http:\/\/openenergy-platform\.org\/ontology\/
IRI_ONTOLOGY := $(IRI_BASE)$(ONTOLOGY_NAME)
SEPARATOR := \/

OWL_COPY := $(OWL_FILES)

OMN_COPY :=	$(OMN_FILES)

TTL_COPY :=	$(TTL_FILES)

OMN_TRANSLATE := ${patsubst %.omn,%.owl,$(OMN_FILES)}
TTL_TRANSLATE := $(call subst_paths_owl,$(TTL_COPY))


RM=/bin/rm
ROBOT_PATH := robot.jar
ROBOT := java -jar $(ROBOT_PATH)

HERMIT_PATH := hermit.jar
HERMIT := java -jar $(HERMIT_PATH)

define replace_devs
	sed -i -E "s/$(OEP_BASE)\/dev\/([a-zA-Z/\.\-]+)/$(OEP_BASE)\/releases\/$(VERSION)\/\1/m" $1
endef

define replace_oms
	sed -i -E "s/($(OEP_BASE)\/dev\/([a-zA-Z/\-]+)\.)omn/\1owl/m" $1
	sed -i -E "s/($(OEP_BASE)\/releases\/$(VERSION)\/([a-zA-Z/\-]+)\.)omn/\1owl/m" $1
endef

define replace_ttls
	sed -i -E "s/($(OEP_BASE)\/dev\/([a-zA-Z/\-]+)\.)ttl/\1owl/m" $1
	sed -i -E "s/($(OEP_BASE)\/releases\/$(VERSION)\/([a-zA-Z/\-]+)\.)ttl/\1owl/m" $1
endef

define replace_owls
	sed -i -E "s/($(OEP_BASE)\/dev\/([a-zA-Z/\-]+)\.)owl/\1ttl/m" $1
	sed -i -E "s/($(OEP_BASE)\/releases\/$(VERSION)\/([a-zA-Z/\-]+)\.)owl/\1ttl/m" $1
endef

define translate_to_owl
	$(ROBOT) convert --catalog $(VERSIONDIR)/catalog-v001.xml --input $2 --output $1 --format owl
	$(call replace_ttls,$1)
	$(call replace_devs,$1)
endef

define translate_to_ttl
	$(ROBOT) convert --catalog $(VERSIONDIR)/catalog-v001.xml --input $2 --output $1 --format ttl
	$(call replace_owls,$1)
	$(call replace_devs,$1)
endef

define translate_to_omn
	$(ROBOT) convert --catalog $(VERSIONDIR)/catalog-v001.xml --input $2 --output $1 --format omn
	$(call replace_owls,$1)
	$(call replace_devs,$1)
endef

.PHONY: all clean base merge directories

all: base merge profiles closure

imports: directories ${TMP}/catalog.xml $(IMPORTS)/bfo-core.ttl $(IMPORTS)/cco-extracted.ttl $(IMPORTS)/oeo-extracted.ttl $(IMPORTS)/iao-extracted.ttl

base: | directories $(VERSIONDIR)/catalog-v001.xml robot.jar  $(TTL_COPY) $(OWL_COPY) $(OWLVERSION) $(TTL_TRANSLATE)

merge: | $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl 

closure: | $(VERSIONDIR)/$(ONTOLOGY_NAME)-closure.ttl

profiles: | $(VERSIONDIR)/$(ONTOLOGY_NAME)-el.ttl $(VERSIONDIR)/$(ONTOLOGY_NAME)-ql.ttl

clean:
	- $(RM) -r $(VERSIONDIR)
	- $(RM) -r ${TMP}
clean-imports:
	- $(RM) -r $(IMPORTS)/*

directories: ${VERSIONDIR}/imports ${VERSIONDIR}/modules ${TMP} $(VERSIONDIR)/owl

$(IMPORTS)/bfo-core.ttl:
	curl -L -o $@ https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/$(BFOCOMMIT)/imports/bfo-core.ttl

$(IMPORTS)/cco-extracted.ttl: $(ROBOT_PATH)
	bash scripts/cco-imports/cco-extracted.sh

$(IMPORTS)/oeo-extracted.ttl: $(ROBOT_PATH)
	bash scripts/oeo-imports/oeo-extracted.sh

$(IMPORTS)/iao-extracted.ttl: $(ROBOT_PATH)
	bash scripts/oeo-imports/iao-extracted.sh

${TMP}:
	${MKDIR_P} ${TMP}

${TMP}/catalog.xml:
	cp assets/catalog.xml  $@

$(VERSIONDIR)/owl:
	${MKDIR_P} $(VERSIONDIR)/owl

${VERSIONDIR}/imports:
	${MKDIR_P} ${VERSIONDIR}/imports

${VERSIONDIR}/modules:
	${MKDIR_P} ${VERSIONDIR}/modules

$(VERSIONDIR)/catalog-v001.xml: $(ONTOLOGY_SOURCE)/catalog-v001.xml
	cp $< $@
	$(call replace_devs,$@)
	sed -i -E "s/edits\//modules\//m" $@

$(ROBOT_PATH): | build
	curl -L -o $@ https://github.com/ontodev/robot/releases/download/v1.9.5/robot.jar

$(HERMIT_PATH): | build
	curl -L -o $@ https://github.com/owlcs/releases/raw/master/HermiT/org.semanticweb.hermit-packaged-1.4.6.519-SNAPSHOT.jar

$(VERSIONDIR)/owl/%.owl: $(VERSIONDIR)/%.ttl
	$(call translate_to_owl,$@,$<)

$(VERSIONDIR)/owl/modules/%.owl: $(VERSIONDIR)/edits/%.ttl
	$(call translate_to_owl,$@,$<)

$(VERSIONDIR)/owl/%.owl: $(ONTOLOGY_SOURCE)/%.owl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/owl/modules/%.owl: $(ONTOLOGY_SOURCE)/edits/%.owl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/modules/%.ttl: $(ONTOLOGY_SOURCE)/edits/%.ttl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/%.ttl: $(ONTOLOGY_SOURCE)/%.ttl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl : | base
	$(ROBOT) merge --catalog $(VERSIONDIR)/catalog-v001.xml $(foreach f, $(VERSIONDIR)/$(ONTOLOGY_NAME).ttl $(TTL_COPY) $(OWL_COPY), --input $(f)) annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@
	$(call replace_ttls,$@)

$(VERSIONDIR)/owl/$(ONTOLOGY_NAME)-full.owl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl
	$(call translate_to_ttl,$@,$<)
	$(call replace_owls,$@)

$(VERSIONDIR)/$(ONTOLOGY_NAME)-closure.ttl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl
	$(ROBOT) reason --input $< --reasoner hermit --catalog $(VERSIONDIR)/catalog-v001.xml --axiom-generators "SubClass EquivalentClass DataPropertyCharacteristic EquivalentDataProperties SubDataProperty ClassAssertion EquivalentObjectProperty InverseObjectProperties ObjectPropertyCharacteristic SubObjectProperty ObjectPropertyRange ObjectPropertyDomain" --include-indirect true annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@
	$(ROBOT) merge --catalog $(VERSIONDIR)/catalog-v001.xml --input $< --input $@ annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@

$(VERSIONDIR)/$(ONTOLOGY_NAME)-el.ttl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl
	$(ROBOT) remove --input $< --catalog $(VERSIONDIR)/catalog-v001.xml --axioms "InverseObjectProperties FunctionalObjectProperty InverseFunctionalObjectProperty" annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@

$(VERSIONDIR)/$(ONTOLOGY_NAME)-ql.ttl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl
	$(ROBOT) reduce --reasoner hermit --input $< --catalog $(VERSIONDIR)/catalog-v001.xml relax remove --axioms "TransitiveObjectProperty FunctionalObjectProperty InverseFunctionalObjectProperty" annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@
