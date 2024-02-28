# TODO and development roadmap

## 28.02.2024

Added documentation online [in gitlab
pages](https://ensym.pages.gitlab.dlr.de/lod/charging-ontology/). I Figured out
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

- [x] Set documentation environment up using [mkdocs](https://www.mkdocs.org/)~~, and probably the [gitbook theme](https://gitlab.com/lramage/mkdocs-gitbook-theme)~~.
- [ ] Setup of the testing framework using competency questions.
- [ ] Write down the use case scenarios (these are also going in the paper).
- [X] Decide in a proper name (CHIO?)
- [X] Decide on the ontology term conventions, maybe use identifiers with the following form "CHIO_XXXXXXXX"
- [ ] Import the necessary OEO Terms.
