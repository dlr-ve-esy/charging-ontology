# Application scenarios

To aid the ontology development and setting the boundaries on what belongs what
doesn't we rely in application scenarios which are textual descriptions of
situations in which the ontology might be used. These descriptions are then
complemented with [competency
questions (CQs)](https://doi.org/10.1016/j.websem.2019.100534) derived from them.
These scenarios are not exhaustive, feel free to propose both real and
theoretical scenarios.

## Scenario 1 - The charging infrastructure register

### Summary

This scenario is heavily inspired by the [German charging infrastructure
register](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/start.html),
and it probably captures most of the requirements of this ontology. The
scenario covers terminology and axioms necessary to perform descriptions in
regard to where infrastructure is found, which power they are able to deliver
and what kind of connector they have.

### Description

A government agency is responsible for the enforcement and monitoring of the
implementation of a law that intends to ensure the availability of **public**
battery electric vehicles charging infrastructure. As part of their success
reporting channels, they offer a data register where stakeholders can consult
the availability and development of said infrastructure. The data contained in
these reports can be used to evaluate spatial and temporal distribution,
technical properties of the infrastructure, numbers per operator, charging
capacities among other things. Stakeholders can use this information in their
decision-making process to contribute to the realization of the law associated
with the register. Citizens, government and independent parties can consult the
data to ensure that the law is working as intended and can be used as part of a
feedback loop for future improvements. Electric vehicle users can consult the
register in their travel decisions, but this is not the main application as
there are other tools for such queries, most of which are available in the
vehicles themselves.

The information detail expected in such dataset has different dimensions. First
and probably the most relevant is geospatial data, such as addresses and
coordinates; land use polygons could be of interest but not for all
applications. Secondly are details about the operation, such as
commissioning/decommissioning dates and operators. Lastly are technical details
interesting for other parties, for example the kind of connectors that are
compatible with a station, since not all autos have the same kind of
connection, current type and charging capacity are interesting for both grid
operators and road infrastructure managers. Detailed description of the
infrastructure capacity such as number of columns and parking places per
installation can be also of interest.

Since this registry is intended to provide visibility of the infrastructure.
Information of the daily operation of the infrastructure is not so relevant,
specially because such data can very rapidly enter the realm of big data. But
such conditions are explored in other scenarios.

### Competency questions

???+ question "Competency question 1.0"

    How many charging points has <this charging station>?

???+ question "Competency question 1.1"

    How many charging columns has <this charging station>?

???+ question "Competency question 1.2"

    Can I plug in <this plug> in <this charging station>?

???+ question "Competency question 1.3"

    Which operator operates <this charging station>?

???+ question "Competency question 1.4"

    When was this charging station commissioned?

???+ question "Competency question 1.5"

    How much power can <this charging station> pull from the electrical grid it is connected to?

???+ question "Competency question 1.6"

    At which rate can <this charging station> charge <this vehicle>?

???+ question "Competency question 1.7"

    How many cars can <this charging station> supply at any given time?

???+ question "Competency question 1.8"

    In which current system does <this charging point> operates?

???+ question "Competency question 1.9"

    What is the number of charging stations located at <this region>?

???+ question "Competency question 1.10"

    How many charging columns are availible at <this address>?

???+ question "Competency question 1.11"

    What are the coordinates of <this station>?

???+ question "Competency question 1.12"

    How many parking places does <this charging station> have?

## Scenario 2 - My awesome scenario

### Summary

Some short description of the scenario, where does it come from and what use
cases it intends to cover.

### Description

The main text of the scenario, be as specific as possible, this section can be
a citation from some paper or other kind of content.

### Competency questions

List of competency questions in plain text, they don't need to be strictly
questions, they can also be affirmations. For example:

> - Is a dog considered a passenger?
> - A shopping trip is a leisure trip