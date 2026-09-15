"""Exécute les requêtes SPARQL de queries/ sur le graphe inféré (ou brut à défaut).

Usage : python scripts/query.py [fichier.rq ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
INFERRED = ROOT / "build" / "ecommerce-inferred.ttl"
RAW = ROOT / "ontology" / "ecommerce.ttl"


def fmt(value) -> str:
    if value is None:
        return ""
    py = value.toPython()
    if isinstance(py, float) or type(py).__name__ == "Decimal":
        return f"{float(py):,.2f}".replace(",", " ")
    return str(py)


def print_table(result) -> None:
    headers = [str(v) for v in result.vars]
    rows = [[fmt(row[v]) for v in result.vars] for row in result]
    widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h) for i, h in enumerate(headers)]
    line = lambda cells: "  ".join(c.ljust(w) for c, w in zip(cells, widths))
    print(line(headers))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(line(r))


def main() -> None:
    source = INFERRED if INFERRED.exists() else RAW
    if source is RAW:
        print("⚠ Graphe inféré absent : lancez d'abord scripts/reason.py (requêtes 01-02 incomplètes)\n")
    graph = Graph().parse(source)
    files = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "queries").glob("*.rq"))
    for f in files:
        print(f"## {f.name}")
        print_table(graph.query(f.read_text(encoding="utf-8")))
        print()


if __name__ == "__main__":
    main()
