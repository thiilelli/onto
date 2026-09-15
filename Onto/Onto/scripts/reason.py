"""Vérifie la cohérence de l'ontologie et matérialise les inférences (Pellet + règles SWRL).

Usage : python scripts/reason.py [--output build/ecommerce-inferred.ttl]
"""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import owlready2
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "ecommerce.ttl"
NS = "https://thiilelli.github.io/Onto/ontology#"

INFERRED_CLASSES = ["CommandePrioritaire", "ProduitVendable", "CommandeValide"]


def load_world(graph: Graph | None = None) -> tuple[owlready2.World, owlready2.Ontology]:
    """Charge un graphe rdflib (par défaut l'ontologie du dépôt) dans un World owlready2 isolé."""
    graph = graph if graph is not None else Graph().parse(ONTOLOGY)
    with tempfile.NamedTemporaryFile(suffix=".nt", delete=False) as tmp:
        graph.serialize(tmp.name, format="nt", encoding="utf-8")
    world = owlready2.World()
    onto = world.get_ontology(f"file://{tmp.name}").load(format="ntriples")
    return world, onto


def reason(world: owlready2.World) -> None:
    """Lance Pellet ; lève OwlReadyInconsistentOntologyError si l'ontologie est incohérente."""
    with world.get_ontology(NS):
        owlready2.sync_reasoner_pellet(world, infer_property_values=True, debug=0)


def members(world: owlready2.World, cls_name: str) -> list[str]:
    cls = world[NS + cls_name]
    return sorted(ind.name for ind in cls.instances()) if cls is not None else []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "ecommerce-inferred.ttl")
    args = parser.parse_args()

    world, _ = load_world()
    try:
        reason(world)
    except owlready2.OwlReadyInconsistentOntologyError:
        print("✗ Ontologie incohérente")
        raise SystemExit(1)
    print("✓ Ontologie cohérente (Pellet)\n")

    for name in INFERRED_CLASSES:
        print(f"{name:<20} {', '.join(members(world, name)) or '(aucun)'}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".nt", delete=False) as tmp:
        world.save(file=tmp.name, format="ntriples")
    Graph().parse(tmp.name, format="nt").serialize(args.output, format="turtle")
    print(f"\nGraphe inféré écrit dans {args.output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
