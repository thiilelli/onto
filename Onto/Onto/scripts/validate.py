"""Valide les individus de l'ontologie contre les formes SHACL (hypothèse du monde fermé).

Usage : python scripts/validate.py
"""
from __future__ import annotations

from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "ecommerce.ttl"
SHAPES = ROOT / "shapes" / "ecommerce-shapes.ttl"


def run_validation(data: Graph | None = None) -> tuple[bool, str]:
    data = data if data is not None else Graph().parse(ONTOLOGY)
    conforms, _, report = validate(
        data,
        shacl_graph=Graph().parse(SHAPES),
        inference="none",          # sh:class suit déjà rdfs:subClassOf présent dans le graphe
        advanced=True,             # contraintes SPARQL
        allow_warnings=False,
    )
    return conforms, report


def main() -> None:
    conforms, report = run_validation()
    if conforms:
        print("✓ Les données respectent toutes les contraintes SHACL")
    else:
        print(report)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
