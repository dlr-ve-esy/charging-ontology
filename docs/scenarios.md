# Motivating scenarios

To aid the ontology development and setting the boundaries on what belongs what
doesn't we rely in motivating scenarios which are textual descriptions of
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

    A public charging station is part of some transportation infrastructure.

???+ question "Competency question 1.1"

    A charging station has charging columns as parts that can change during its lifetime.

???+ question "Competency question 1.2"

    A charging column has charging points as parts that do not change during its lifetime.

???+ question "Competency question 1.3"

    A charging point is compatible with some plugs.

???+ question "Competency question 1.4"

    A charging station has at least one operator at any given time.

???+ question "Competency question 1.5"

    A charging station has comissioning and decomissioning dates which delimit its lifetime.

???+ question "Competency question 1.6"

    A charging station has a maximum amount of power it can pull from an electric grid.

???+ question "Competency question 1.7"

    A charging point has a maximum amount of power it can supply to a battery.

???+ question "Competency question 1.8"

    A charging point can supply one car at a time.

???+ question "Competency question 1.9"

    A charging point can operate with some current system.

???+ question "Competency question 1.10"

    A charging station is located in some place

???+ question "Competency question 1.11"

    A place can be associated with some address

???+ question "Competency question 1.12"

    A place can be associated with some geograpical feature.

???+ question "Competency question 1.13"

    A charging station has parking places as parts.

???+ question "Competency question 1.14"

    A charging station has a maximum vehicle capacity.


## Scenario 2 - iCity Project Smart Parking Applications

### Summary

This scenario is an extract of the [iCity
project](https://enterpriseintegrationlab.github.io/icity/iCityOntologyReport_1.2.pdf)
by Katsumi and Fox. Particularly the section smart parking applications. This
subset of questions is relevant to us because charging infrastructure is
intimately connected with parking infrastructure. These queries rely a lot in
geographical queries and may overlap with scenario 1, but they have a
perspective more in line with daily operation of the stations. For more details
on the ontology [visit its
repository](https://github.com/EnterpriseIntegrationLab/icity).

### Description

The iCity Transportation Planning Suite of Ontologies was conceived to aid
city-wide Transportation research in the City of Toronto. It has a very wide
scope across the field of transportation planning. Their competency questions
related to parking are a strong starting point to implement its associated
commitments in BFO. Since the structure of the foundational ontology used in
that particular project is significantly different, we are not taking over 100%
of the SPARQL implementation of the questions. Some parking questions like "Is
it accessible by disabled people, and if so how many parking spots are for
disabled vehicles?" were excluded because they are beyond the scope of this
ontology and not because they are irrelevant.

### Competency questions

???+ question "Competency question 2.0"

    What is the address of the parking lot P?

???+ question "Competency question 2.1"

    What is the (vehicle) capacity of parking lot P?

???+ question "Competency question 2.2"

    What are the geographic coordinates for parking lot P?

???+ question "Competency question 2.3"

    Is there a height limit for vehicles for a parking lot P?

???+ question "Competency question 2.4"

    What building is a particular parking lot located in?

???+ question "Competency question 2.5"

    Is a particular parking lot open to the public at a given time?

???+ question "Competency question 2.6"

    How many parking spots are designated for electric vehicles in a particular parking lot?

???+ question "Competency question 2.7"

    What types of electric vehicle chargers are available in a particular parking lot?


## Scenario 3 - Drive2X working package 5 scenario

### Summary

This scenarios is based on work in the EU project Drive2X, specifically working
package 5. In this context, a forecasting method is being developed providing 
aggregated electric load of all charging stations in a defined spatial scope
(e.g. a quarter, a couple of streets, a sub-part of a distribution grid system).
Additionally, the temporal flexibility of this load is given.

### Description

The forecast will be provided for two temporal scopes: For the next day in high
temporal resolution and for the next month in lower resolution. 
The tool will use openly available static data and dynamic data via APIs where
possible and sensible. However, it will also build on historically known data of
charging station electric loads to provide default values where insufficient
live-data is available.

The application will offer a front-end in form of a graphical user interface in
which the users will provide spatial constraints (polygons, points, routes) and
may select charging strategies (as soon as possible, as late as possible, price
oriented etc.). The produced data will consist of indicators describing the
forecast load for the spatial scope, scenarios and associated parameters.

Indicator outputs as well as intermediary data is provided to the user in
graphical and tabular form. A measure for uncertainty of the respective output
will be provided to the user as well. 

### Competency questions

To be completed ...

## Scenario X - My awesome scenario

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
