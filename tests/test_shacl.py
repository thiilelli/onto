"""Tests de validation SHACL (monde fermé)."""
import pytest
from conftest import ECO, add_ttl

from validate import run_validation


def test_dataset_conforms(graph):
    conforms, report = run_validation(graph)
    assert conforms, report


@pytest.mark.parametrize(
    "ttl, expected",
    [
        ("eco:A01 eco:note 7 .", "entre 1 et 5"),
        ('eco:C01 eco:emailClient "pas-un-email" .', "email invalide"),
        ("eco:S05 eco:quantite 45 .", "Capacité dépassée"),
        ('eco:Pay01 eco:datePaiement "2025-01-01T00:00:00"^^xsd:dateTime .', "avant la commande"),
        ('eco:P01 eco:prix "-10.0"^^xsd:decimal .', "prix unique strictement positif"),
    ],
)
def test_invalid_data_is_reported(graph, ttl, expected):
    conforms, report = run_validation(add_ttl(graph, ttl))
    assert not conforms
    assert expected in report


def test_missing_invoice_is_reported(graph):
    # En OWL (monde ouvert) ce n'est pas une incohérence ; en SHACL, si.
    graph.remove((ECO.O02, ECO.genere, None))
    conforms, report = run_validation(graph)
    assert not conforms
    assert "genere" in report
