# %%
import pygraphviz as pgv
import pyhornedowl as pho
from pyhornedowl.model import *
from pathlib import Path
import os

CWD = Path(os.getcwd())
FILEPATH = Path(os.path.dirname(os.path.realpath(__file__)))

# Clunky search for the basedir
if FILEPATH == CWD:
    BASEDIR = Path("../..")
elif "VERSION" in [p.name for p in CWD.iterdir()]:
    BASEDIR = Path(".")

TMP = BASEDIR.joinpath("tmp")
TMP.mkdir(exist_ok=True)

PAPER = BASEDIR.joinpath("paper/images")
PAPER.mkdir(exist_ok=True)

SVG = TMP.joinpath("svg")
SVG.mkdir(exist_ok=True)

PNG = PAPER
PNG.mkdir(exist_ok=True)

DROPLIST = []

PREFIX_MAPPINGS = {
    "http://www.ontologyrepository.com/CommonCoreOntologies/": "CCO:",
    "http://purl.obolibrary.org/obo/": "BFO:",
    "http://openenergy-platform.org/ontology/oeo/": "OEO",
    "http://ontology.eil.utoronto.ca/icity/Parking/": "ICP:",
    "http://ontology.eil.utoronto.ca/icity/Change/": "ICC:",
}
RDFSLABEL = "http://www.w3.org/2000/01/rdf-schema#label"

NL_RENDER = "\\n"  #  \\n for dot to png, \\\\ for dot2tex


# %%
def render_equivalent_class_axiom(G, axiom, ontology, edge_attrs={}, node_attrs={}):
    # This assumes that the left sides are likely classes
    # probably breaks with general axioms
    left_class, right_part = axiom.first
    left_iri = str(left_class.first)
    left_label = get_label(left_iri, ontology)
    if left_label in G.nodes():
        if isinstance(right_part, ObjectIntersectionOf):
            left_res, right_res = right_part.first
            r_res_edge = get_label(str(right_res.ope.first), ontology)
            r_res_node = get_label(str(right_res.bce.first), ontology)
            l_res_edge = get_label(str(left_res.ope.first), ontology)
            l_res_node = get_label(str(left_res.bce.first), ontology)
            if l_res_node in G.nodes():
                G.graph_attr["rank"] = "same"
            G.add_node(r_res_node, **node_attrs)
            SG = G.add_subgraph(
                [left_label, r_res_node],
                style="rounded,dotted",
                label="Equivalence restriction",
                fontcolor="grey",
                fontsize="8",
                labeljust="l",
                name="cluster_restriction",
                rank="same",
                rankdir="TB",
            )
            _ = SG.add_subgraph([left_label, r_res_node], rank="same")
            if (left_label, r_res_node) not in G.edges():
                SG.add_edge(
                    left_label,
                    r_res_node,
                    label=r_res_edge,
                    style="dashed",
                    arrowsize=0.5,
                    penwidth=0.5,
                )


def render_subclass_restriction_axiom(G, axiom, ontology, edge_attrs={}):
    # This assumes that the left sides are likely classes
    # probably breaks with general axioms
    super_class = axiom.sup
    sub_class = axiom.sub
    sub_iri = str(sub_class.first)
    sub_label = get_label(sub_iri, ontology)
    if sub_label in G.nodes():
        if isinstance(super_class, ObjectSomeValuesFrom) or isinstance(
            super_class, ObjectAllValuesFrom
        ):
            bce_iri = str(super_class.bce.first)
            bce_label = get_label(bce_iri, ontology)
            op_iri = str(super_class.ope.first)
            op_label = get_label(op_iri, ontology)
            if bce_label in G.nodes():
                _ = G.add_subgraph([sub_label, bce_label], rank="same")
                _.add_edge(sub_label, bce_label, label=op_label, **edge_attrs)
                G.graph_attr["rank"] = "same"


def add_taxonomy(G, ontology, edge_attrs={}):
    for c in ontology.get_classes():
        if c not in DROPLIST:
            main_label = get_label(c, ontology)
            G.add_node(main_label)
            for sc in ontology.get_subclasses(c):
                if sc not in DROPLIST:
                    sc_label = get_label(sc, ontology)
                    G.add_node(sc_label)
                    G.add_edge(main_label, sc_label, **edge_attrs)


def get_label(iri, ontology):
    label = None
    for mapping, prefix in PREFIX_MAPPINGS.items():
        if mapping in iri:
            label = iri.replace(mapping, prefix)
    if label is None:
        label = iri
    if " " in label:
        label = " ".join([p for p in label.split(" ")])
    if len(label) > 10:
        label = f"{NL_RENDER}".join([p for p in label.split(" ")])
    return label


# %%
parking = pho.open_ontology(TMP.joinpath("parking_space.owx").as_posix())

PG = pgv.AGraph(
    strict=False, directed=True, name="G", layout="dot", splines=True, rankdir="TB"
)
# 4.70
# PG.graph_attr["ratio"] = "compressed"
PG.graph_attr["size"] = "8.24,5.78"
PG.graph_attr["dpi"] = "400"
PG.graph_attr["nodesep"] = "0.1"
PG.graph_attr["ranksep"] = "0.1"
PG.node_attr["fontsize"] = "10"
PG.node_attr["fontname"] = "CMU Serif Roman"
PG.node_attr["shape"] = "ellipse"
PG.edge_attr["fontsize"] = "10"
PG.edge_attr["fontname"] = "CMU Serif Roman"
PG.edge_attr["arrowsize"] = "0.5"

edge_attrs = dict(style="dashed", arrowsize=0.5, penwidth=0.59)
add_taxonomy(
    PG,
    parking,
    edge_attrs={"color": "black", "splines": "curved", "penwidth": "0.8"},
)
props = [
    "http://ontology.eil.utoronto.ca/icity/Change/manifestationOf",
    "http://ontology.eil.utoronto.ca/icity/Change/hasManifestation",
    "http://ontology.eil.utoronto.ca/icity/Parking/hasParkingPolicy",
    "http://ontology.eil.utoronto.ca/icity/Parking/hasEVCharger",
]
for prop in props:
    for aa in parking.get_axioms_for_iri(prop):
        if isinstance(aa.axiom, SubClassOf):
            render_subclass_restriction_axiom(
                PG, aa.axiom, parking, edge_attrs=edge_attrs
            )
        if isinstance(aa.axiom, EquivalentClasses):
            render_equivalent_class_axiom(PG, aa.axiom, parking)
PG.write(TMP.joinpath("PARKING.dot").as_posix())
PG.draw(SVG.joinpath("PARKING.svg").as_posix(), prog="dot")
PG.draw(PNG.joinpath("PARKING.png").as_posix(), prog="dot")

# %%
