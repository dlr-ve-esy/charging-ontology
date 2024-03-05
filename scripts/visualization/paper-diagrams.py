# %%
import pygraphviz as pgv
import pyhornedowl as pho
from pyhornedowl.model import *

PREFIX_MAPPINGS = {
    "http://www.ontologyrepository.com/CommonCoreOntologies/": "CCO:",
    "http://purl.obolibrary.org/obo/": "BFO:",
    "http://openenergy-platform.org/ontology/oeo/": "OEO",
}
RDFSLABEL = "http://www.w3.org/2000/01/rdf-schema#label"

DROPLIST = [
    "http://purl.obolibrary.org/obo/BFO_0000023",
    "http://openenergy-platform.org/ontology/oeo/OEO_00000068",
]

BFO2020_MAPPINGS = {
    "http://purl.obolibrary.org/obo/BFO_0000051": "http://purl.obolibrary.org/obo/BFO_0000178"
}
# %%
bfo = pho.open_ontology("tmp/bfo.owx")
ontology = pho.open_ontology("tmp/ao_infrastructure.owx")


# %%
def get_label(iri, ontology):
    if iri in BFO2020_MAPPINGS:
        iri = BFO2020_MAPPINGS[iri]
    label = ontology.get_annotation(iri, RDFSLABEL)
    if label is None:
        label = bfo.get_annotation(iri, RDFSLABEL)
    if label is None:
        for mapping, prefix in PREFIX_MAPPINGS.items():
            if mapping in iri:
                label = iri.replace(mapping, prefix)
    if label is None:
        label = iri
    if " " in label:
        label = " ".join([p.lower() for p in label.split(" ")])
    if len(label) > 10:
        label = "\\n".join([p.lower() for p in label.split(" ")])
    return label


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


def find_equivalent_class_axioms(iri, ontology):
    eq_classes = [
        a.axiom
        for a in ontology.get_axioms_for_iri(
            "http://purl.obolibrary.org/obo/BFO_0000196"
        )
        if isinstance(a.axiom, EquivalentClasses)
    ]
    return eq_classes


def render_simple_class(G, cls, left_label, ontology, edge_attrs={}):
    iri = str(cls.first[0].first)
    label = get_label(iri, ontology)
    G.add_node(label)
    return label


def render_equivalent_class_axiom(G, axiom, ontology, edge_attrs={}, node_attrs={}):
    # This assumes that the left sides are likely classes
    # probably breaks with general axioms
    left_class, right_part = axiom.first
    left_iri = str(left_class.first)
    left_label = get_label(left_iri, ontology)
    if left_label in G.nodes():
        if isinstance(right_part, ObjectIntersectionOf):
            base_class, restriction = right_part.first
            res_edge = get_label(str(restriction.ope.first), ontology)
            res_node = get_label(str(restriction.bce.first), ontology)
            base_label = get_label(str(base_class.first), ontology)
            if base_label in G.nodes():
                G.graph_attr["rank"] = "same"
            G.add_node(res_node, **node_attrs)
            SG = G.add_subgraph(
                [left_label, res_node],
                style="rounded,dotted",
                label="Equivalence restriction",
                fontcolor="grey",
                fontsize="8",
                labeljust="l",
                name="cluster_restriction",
                rank="same",
                rankdir="TB",
            )
            _ = SG.add_subgraph([left_label, res_node], rank="same")
            if (left_label, res_node) not in G.edges():
                SG.add_edge(
                    left_label,
                    res_node,
                    label=res_edge,
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
        if isinstance(super_class, ObjectSomeValuesFrom):
            bce_iri = str(super_class.bce.first)
            bce_label = get_label(bce_iri, ontology)
            op_iri = str(super_class.ope.first)
            op_label = get_label(op_iri, ontology)
            if bce_label in G.nodes():
                _ = G.add_subgraph([sub_label, bce_label], rank="same")
                _.add_edge(sub_label, bce_label, label=op_label, **edge_attrs)
                G.graph_attr["rank"] = "same"


# %%
object_properties = ontology.get_object_properties()


# %% [markdown]
# ## Test rendering
# This script renders the axioms from "infrastructure system" as a test of the
# combination of py-horned-owl and py-graphviz.
# %%
G = pgv.AGraph(strict=True, directed=True, name="G", layout="dot", splines=True)
G.graph_attr["ratio"] = "0.52"
G.graph_attr["nodesep"] = "0.4"
G.graph_attr["ranksep"] = "0.1"
G.node_attr["fontsize"] = "10"
G.node_attr["fontname"] = "CMU Serif Roman"
G.node_attr["shape"] = "ellipse"
G.edge_attr["fontsize"] = "10"
G.edge_attr["fontname"] = "CMU Serif Roman"
G.edge_attr["arrowsize"] = "0.5"
add_taxonomy(
    G,
    ontology,
    edge_attrs={"color": "black", "splines": "curved", "penwidth": "0.8"},
)
axiom = find_equivalent_class_axioms(
    "http://www.ontologyrepository.com/CommonCoreOntologies/InfrastructureElement",
    ontology,
)[0]
render_equivalent_class_axiom(
    G,
    axiom,
    ontology,
    node_attrs=dict(
        shape="ellipse", style="dashed", fixedsize=False, fontsize=8, color="grey"
    ),
)
G.write("infrastructureSystem.dot")
# %% [markdown]
# ## Render OEO imported commitments
# Imported classes like battery
# combination of py-horned-owl and py-graphviz.
# %%
oeo_vehicle_imports = pho.open_ontology("tmp/oeo_vehicle.owx")

OG = pgv.AGraph(
    strict=False, directed=True, name="G", layout="dot", splines=True, rankdir="LR"
)
OG.graph_attr["ratio"] = "compressed"
OG.graph_attr["nodesep"] = "0.4"
OG.graph_attr["ranksep"] = "0.1"
OG.node_attr["fontsize"] = "10"
OG.node_attr["fontname"] = "CMU Serif Roman"
OG.node_attr["shape"] = "ellipse"
OG.edge_attr["fontsize"] = "10"
OG.edge_attr["fontname"] = "CMU Serif Roman"
OG.edge_attr["arrowsize"] = "0.5"

edge_attrs = dict(style="dashed", arrowsize=0.5, penwidth=0.59)
add_taxonomy(
    OG,
    oeo_vehicle_imports,
    edge_attrs={"color": "black", "splines": "curved", "penwidth": "0.8"},
)
for aa in oeo_vehicle_imports.get_axioms_for_iri(
    "http://purl.obolibrary.org/obo/BFO_0000051"
):
    if isinstance(aa.axiom, SubClassOf):
        render_subclass_restriction_axiom(
            OG, aa.axiom, oeo_vehicle_imports, edge_attrs=edge_attrs
        )
    if isinstance(aa.axiom, EquivalentClasses):
        render_equivalent_class_axiom(OG, aa.axiom, oeo_vehicle_imports)
OG.write("OEOVehicle.dot")
# %% [markdown]
# ## Render Vehicle Taxonomy
# Render the taxonomy from CCO
# %%
vehicle_tax_cco = pho.open_ontology("tmp/ao_vehicles.owx")
VG = pgv.AGraph(
    strict=False, directed=True, name="G", layout="dot", splines=True, rankdir="TB"
)
VG.graph_attr["ratio"] = "compressed"
VG.graph_attr["nodesep"] = "0.4"
VG.graph_attr["ranksep"] = "0.1"
VG.node_attr["fontsize"] = "10"
VG.node_attr["fontname"] = "CMU Serif Roman"
VG.node_attr["shape"] = "ellipse"
VG.edge_attr["fontsize"] = "10"
VG.edge_attr["fontname"] = "CMU Serif Roman"
VG.edge_attr["arrowsize"] = "0.5"

edge_attrs = dict(style="dashed", arrowsize=0.5, penwidth=0.59)
add_taxonomy(
    VG,
    vehicle_tax_cco,
    edge_attrs={"color": "black", "splines": "curved", "penwidth": "0.8"},
)
VG.write("CCOVehicles.dot")

# %%
