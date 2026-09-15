import sys
from pathlib import Path

import pytest
from rdflib import Graph, Namespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

ECO = Namespace("https://thiilelli.github.io/Onto/ontology#")
PREFIXES = (
    "@prefix eco: <https://thiilelli.github.io/Onto/ontology#> .\n"
    "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
)


@pytest.fixture
def graph() -> Graph:
    """Copie fraîche de l'ontologie, modifiable par chaque test."""
    return Graph().parse(ROOT / "ontology" / "ecommerce.ttl")


def add_ttl(g: Graph, ttl: str) -> Graph:
    g.parse(data=PREFIXES + ttl, format="turtle")
    return g
