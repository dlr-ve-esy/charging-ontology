ONTOLOGY_NAME := chio
MKDIR_P = mkdir -p
VERSION:= $(shell cat VERSION)
VERSIONDIR := build/chio/$(VERSION)
ONTOLOGY_SOURCE := src
BFOCOMMIT := d9aa636303766bfb6a7a6d46265873f96cdd8584

subst_paths =	${subst $(ONTOLOGY_SOURCE),$(VERSIONDIR),${patsubst $(ONTOLOGY_SOURCE)/edits/%,$(ONTOLOGY_SOURCE)/modules/%,$(1)}}

OWL_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)/* -type f -name "*.owl"))
OMN_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)/* -type f -name "*.omn"))
TTL_FILES := $(call subst_paths,$(shell find $(ONTOLOGY_SOURCE)/* -type f -name "*.ttl"))

IRI_BASE := http:\/\/openenergy-platform\.org\/ontology\/
IRI_ONTOLOGY := $(IRI_BASE)$(ONTOLOGY_NAME)
SEPARATOR := \/

OWL_COPY := $(OWL_FILES)

OMN_COPY :=	$(OMN_FILES)

TTL_COPY :=	$(TTL_FILES)

OMN_TRANSLATE := ${patsubst %.omn,%.owl,$(OMN_FILES)}
TTL_TRANSLATE := ${patsubst %.ttl,%.owl,$(TTL_FILES)}

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

all: base merge closure

imports: src/imports/bfo-core.ttl

base: | directories $(VERSIONDIR)/catalog-v001.xml robot.jar $(OWL_COPY) $(TTL_COPY) $(TTL_TRANSLATE)

merge: | $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl

closure: | $(VERSIONDIR)/$(ONTOLOGY_NAME)-closure.owl

clean:
	- $(RM) -r $(VERSIONDIR)

directories: ${VERSIONDIR}/imports ${VERSIONDIR}/modules

src/imports/bfo-core.ttl:
	curl -L -o $@ https://raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/$(BFOCOMMIT)/imports/bfo-core.ttl

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

$(VERSIONDIR)/%.owl: $(VERSIONDIR)/%.ttl
	$(call translate_to_owl,$@,$<)

$(VERSIONDIR)/modules/%.owl: $(VERSIONDIR)/edits/%.ttl
	$(call translate_to_owl,$@,$<)

$(VERSIONDIR)/%.owl: $(ONTOLOGY_SOURCE)/%.owl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/modules/%.owl: $(ONTOLOGY_SOURCE)/edits/%.owl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/modules/%.ttl: $(ONTOLOGY_SOURCE)/edits/%.ttl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/%.ttl: $(ONTOLOGY_SOURCE)/%.ttl
	cp -a $< $@
	$(call replace_devs,$@)

$(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl : | base
	$(ROBOT) merge --catalog $(VERSIONDIR)/catalog-v001.xml $(foreach f, $(VERSIONDIR)/$(ONTOLOGY_NAME).owl $(TTL_COPY) $(OWL_COPY), --input $(f)) annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@
	$(call replace_ttls,$@)

$(VERSIONDIR)/$(ONTOLOGY_NAME)-full.owl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.ttl
	$(call translate_to_ttl,$@,$<)
	$(call replace_owls,$@)

$(VERSIONDIR)/$(ONTOLOGY_NAME)-closure.owl : $(VERSIONDIR)/$(ONTOLOGY_NAME)-full.owl
	$(ROBOT) reason --input $< --reasoner hermit --catalog $(VERSIONDIR)/catalog-v001.xml --axiom-generators "SubClass EquivalentClass DataPropertyCharacteristic EquivalentDataProperties SubDataProperty ClassAssertion EquivalentObjectProperty InverseObjectProperties ObjectPropertyCharacteristic SubObjectProperty ObjectPropertyRange ObjectPropertyDomain" --include-indirect true annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@
	$(ROBOT) merge --catalog $(VERSIONDIR)/catalog-v001.xml --input $< --input $@ annotate --ontology-iri $(IRI_ONTOLOGY)$(SEPARATOR) --output $@