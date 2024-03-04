# %%
import pygraphviz as pgv
import pyhornedowl as pho
from pyhornedowl.model import *

PREFIX_MAPPINGS = {
    "http://www.ontologyrepository.com/CommonCoreOntologies/": "CCO:",
    "http://purl.obolibrary.org/obo/": "BFO:",
}
RDFSLABEL = "http://www.w3.org/2000/01/rdf-schema#label"

DROPLIST = ""
# %%
bfo = pho.open_ontology("tmp/bfo.owx")
ontology = pho.open_ontology("tmp/ao_infrastructure.owx")


# %%
def get_label(iri):
    label = ontology.get_annotation(iri, RDFSLABEL)
    if label is None:
        label = bfo.get_annotation(iri, RDFSLABEL)
    if label is None:
        for mapping, prefix in PREFIX_MAPPINGS.items():
            if mapping in iri:
                label = iri.replace(mapping, prefix)
    if label is None:
        label = iri
    return label


def add_taxonomy(G, ontology, edge_attrs={}):
    for c in ontology.get_classes():
        main_label = get_label(c)
        G.add_node(main_label)
        for sc in ontology.get_subclasses(c):
            sc_label = get_label(sc)
            G.add_node(sc_label)
            G.add_edge(main_label, sc_label, **edge_attrs)


def find_equivalent_class_axioms(iri):
    eq_classes = [
        a.axiom
        for a in ontology.get_axioms_for_iri(
            "http://purl.obolibrary.org/obo/BFO_0000196"
        )
        if isinstance(a.axiom, EquivalentClasses)
    ]
    return eq_classes


def render_simple_class(G, cls, left_label, edge_attrs={}):
    iri = str(cls.first[0].first)
    label = get_label(iri)
    G.add_node(label)
    G.add_edge(left_label, label, **edge_attrs)


def render_object_intersection(G, oi, left_label, edge_attrs={}):
    pass


render_map = {
    Class: render_simple_class,
    ObjectIntersectionOf: render_object_intersection,
}

edge_props_map = {
    Class: {},
    ObjectIntersectionOf: {},
}


def render_equivalent_class_axiom(G, axiom, edge_attrs={}):
    # This assumes that the left sides are likely classes
    # probably breaks with general axioms
    left_class, right_part = axiom.first
    left_iri = str(left_class.first[0].first)
    left_label = get_label(left_iri)
    G.add_node(left_label)
    renderer = render_map.get(type(right_part), lambda x: None)
    edge_props = edge_props_map.get(type(right_part), {})
    renderer(G, left_label, right_part, **edge_props)


# %%
object_properties = ontology.get_object_properties()


# %%
G = pgv.AGraph(strict=False, directed=True)
add_taxonomy(G, ontology, edge_attrs={"color": "blue"})
G.write("hi.dot")

# %%
