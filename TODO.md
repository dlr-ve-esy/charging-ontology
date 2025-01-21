# TODO and development roadmap

## 04.04.2024

A lot of development has happened, since I am using GitHub to document ideas and implementations this TODO is going slowly obsolete. The idea is to replace it with a CHANGELOG during the initial release.

## 18.03.2024

- [ ] Important question: is every transportation facility part of some transportation infrastructure?
- [ ] Import from RO: has role, has quality etc...

## 07.03.2024

- [X] Reworked pipeline

## 07.03.2024

- [ ] Follow this to avoid botching parking ontology: https://github.com/ontodev/robot/issues/1150

## 05.03.2024

Produced first version of paper diagrams. These show the commitments of
existing ontologies. 

- [ ] Produce diagrams of implementations from this ontology.

## 04.03.2024

- [X] Considering importing parking related competency questions from the [iCity
project
report](https://enterpriseintegrationlab.github.io/icity/iCityOntologyReport_1.2.pdf)

## 03.03.2024

Implemented a strong basis for imports coming from the CCO and the OEO. There
are still some classes that have to be redefined and added to the ontology as
possible equivalents via annotation properties.

  - [ ] Implement key classes from scenario 1
  - [X] Add potential associations using "may be identical to"

## 01.03.2024

Implemented the imports from CCO and the IAO (used the imports from OEO), I had
to manually add the sub-class relation between the information entities and
BFO. Realized that there are numerous classes from CCO that can be valuable for
this ontology. 

 - [X] I should implement a script that automatically extracts and collects
   subclasses of `change`, `GeographicalLocations` and others.
 - [X] I should add correct attribution to the imported modules.

## 29.02.2024

Imported some concepts from the Common Core Ontologies. This might need an
extra step of replacing the iris when releasing. Also assigned them with
identifiers specific to the current ontology, so they are easily recognizable.

- [ ] Currently the CCO imports cause a duplication of some BFO classes axioms.
  I have to figure out how to make this leaner.

## 28.02.2024

Added documentation online [in gitlab
pages](https://ensym.pages.gitlab.dlr.de/lod/charging-ontology/). 

- [X] I Figured out
I need to rethink the approach for competency questions, this
[paper](https://doi.org/10.1016/j.websem.2019.100534) has good examples of
competency questions and their SPARQL implementation. Maybe I can use it to
inspire the ones in this ontology.

## 27.02.2024

I set everything up to have a working developer documentation, this has still
to be filled with more content.

- [X] Setup CI to render docs.
- [ ] Consider adding documentation versioning.

## 26.02.2024

This ontology project is a small practical application intended for
demonstration of the concepts explored in one of my publications. This should
serve as practice for ontology development. Initial setup requirements:

- [X] Set documentation environment up using [mkdocs](https://www.mkdocs.org/)~~, and probably the [gitbook theme](https://gitlab.com/lramage/mkdocs-gitbook-theme)~~.
- [X] Setup of the testing framework using competency questions.
- [X] Write down the use case scenarios (these are also going in the paper).
- [X] Decide in a proper name (CHIO?)
- [X] Decide on the ontology term conventions, maybe use identifiers with the following form "CHIO_XXXXXXXX"
- [X] Import the necessary OEO Terms.
