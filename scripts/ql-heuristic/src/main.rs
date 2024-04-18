use horned_owl::io::{owx::reader, ParserConfiguration};
use horned_owl::model::*;
use horned_owl::ontology::component_mapped::RcComponentMappedOntology;
use std::fs::File;
use std::io::BufReader;

fn main() {
    let ontology_path: &str = "../../build/chio/0.1.0/owx/chio-full.owx";
    let file = File::open(&ontology_path).unwrap();
    let mut bufreader = BufReader::new(file);
    let (ont, _) = reader::read(&mut bufreader, ParserConfiguration::default()).unwrap();

    let mut amo: RcComponentMappedOntology = ont.into();

    for c in amo.into_iter() {
        match &c.component {
            Component::TransitiveObjectProperty(top) => amo.remove(),
            Component::InverseFunctionalObjectProperty(ifop) => (),
            Component::SubClassOf(SubClassOf { sup, sub }) => {
                match sup {
                    ClassExpression::ObjectAllValuesFrom{ope: a, bce: b} => (),
                    _ => ()
                };
            },
            Component::ObjectPropertyDomain(ObjectPropertyDomain{ope: op, ce: cc}) => {
                match cc {
                    ClassExpression::ObjectUnionOf(vc) => println!("{:?}", vc),
                    _ => ()
                };
            },
            _ => (),
        }
    }
}
