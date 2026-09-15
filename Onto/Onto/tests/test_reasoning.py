"""Tests OWL + SWRL (Pellet via owlready2 ; nécessite Java)."""
import owlready2
import pytest
from conftest import ECO, add_ttl

from reason import load_world, members, reason


def run(graph):
    world, _ = load_world(graph)
    reason(world)
    return world


def test_ontology_is_consistent(graph):
    run(graph)


def test_rule_r1_priority_orders(graph):
    assert members(run(graph), "CommandePrioritaire") == ["O01"]


def test_rule_r2_sellable_products_exclude_out_of_stock(graph):
    # P04 (stock S04 à 0) ne doit pas être inféré vendable
    assert members(run(graph), "ProduitVendable") == ["P01", "P02", "P03", "P05"]


def test_rule_r3_valid_orders(graph):
    assert members(run(graph), "CommandeValide") == ["O01", "O02"]


def test_rule_r3_requires_payment(graph):
    graph.remove((ECO.O02, ECO.estPayeePar, None))
    graph.remove((None, ECO.regle, ECO.O02))
    assert members(run(graph), "CommandeValide") == ["O01"]


@pytest.mark.parametrize(
    "ttl, reason_",
    [
        ("eco:S01 eco:concerneProduit eco:P03 .", "un stock concerne exactement un produit"),
        ("eco:S02 eco:estStockeDans eco:E01 .", "un stock est dans exactement un entrepôt"),
        ("eco:C01 a eco:Produit .", "Client et Produit sont disjoints"),
        ("eco:Fa02 eco:note 2 .", "note a pour domaine Avis, disjoint de Facture"),
        ("eco:L01 a eco:LivraisonStandard .", "Express et Standard sont disjointes"),
    ],
)
def test_modelling_errors_make_ontology_inconsistent(graph, ttl, reason_):
    add_ttl(graph, ttl)
    with pytest.raises(owlready2.OwlReadyInconsistentOntologyError):
        run(graph)
