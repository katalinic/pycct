from pycct import (
    DoublePushoutRule,
    FinGraphMorphism,
    FinGraphObject,
    FinSetMorphism,
    FinSetObject,
    double_pushout,
)


def test_dpo():
    condition_nodes = FinSetObject(["A", "B", "C", "D", "E", "G", "H", "I", "J", "K"])
    precondition_nodes = FinSetObject(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
    postcondition_nodes = FinSetObject(["A", "B", "C", "D", "E", "G", "H", "I", "J", "K", "L"])
    before_nodes = FinSetObject(
        [
            frozenset({"A"}),
            frozenset({"B"}),
            frozenset({"C", "D"}),
            frozenset({"E"}),
            frozenset({"F"}),
            frozenset({"G"}),
            frozenset({"H"}),
            frozenset({"I"}),
            frozenset({"J"}),
            frozenset({"K"}),
            frozenset({"Z"}),
        ]
    )
    condition_edges = FinSetObject(["DE", "GH1", "GH2"])
    precondition_edges = FinSetObject(["CE", "DE", "EF", "GH1", "GH2", "IJ", "JK"])
    postcondition_edges = FinSetObject(["AB", "DE", "EL", "GH1", "GH2", "IK"])
    before_edges = FinSetObject(
        [
            frozenset({"AB"}),
            frozenset({"AZ"}),
            frozenset({"CE"}),
            frozenset({"DE"}),
            frozenset({"EF"}),
            frozenset({"GH1", "GH2"}),
            frozenset({"IJ"}),
            frozenset({"JK"}),
        ]
    )
    condition_graph = FinGraphObject(
        condition_nodes,
        condition_edges,
        FinSetMorphism(condition_edges, condition_nodes, lambda e: {"DE": "D", "GH1": "G", "GH2": "G"}[e]),
        FinSetMorphism(condition_edges, condition_nodes, lambda e: {"DE": "E", "GH1": "H", "GH2": "H"}[e]),
    )
    precondition_graph = FinGraphObject(
        precondition_nodes,
        precondition_edges,
        FinSetMorphism(
            precondition_edges,
            precondition_nodes,
            lambda e: {"CE": "C", "DE": "D", "EF": "E", "GH1": "G", "GH2": "G", "IJ": "I", "JK": "J"}[e],
        ),
        FinSetMorphism(
            precondition_edges,
            precondition_nodes,
            lambda e: {"CE": "E", "DE": "E", "EF": "F", "GH1": "H", "GH2": "H", "IJ": "J", "JK": "K"}[e],
        ),
    )
    postcondition_graph = FinGraphObject(
        postcondition_nodes,
        postcondition_edges,
        FinSetMorphism(
            postcondition_edges,
            postcondition_nodes,
            lambda e: {"AB": "A", "DE": "D", "EL": "E", "GH1": "G", "GH2": "G", "IK": "I"}[e],
        ),
        FinSetMorphism(
            postcondition_edges,
            postcondition_nodes,
            lambda e: {"AB": "B", "DE": "E", "EL": "L", "GH1": "H", "GH2": "H", "IK": "K"}[e],
        ),
    )
    before_graph = FinGraphObject(
        before_nodes,
        before_edges,
        FinSetMorphism(
            before_edges,
            before_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"A"}),
                frozenset({"AZ"}): frozenset({"A"}),
                frozenset({"CE"}): frozenset({"C", "D"}),
                frozenset({"DE"}): frozenset({"C", "D"}),
                frozenset({"EF"}): frozenset({"E"}),
                frozenset({"GH1", "GH2"}): frozenset({"G"}),
                frozenset({"GH1", "GH2"}): frozenset({"G"}),
                frozenset({"IJ"}): frozenset({"I"}),
                frozenset({"JK"}): frozenset({"J"}),
            }[e],
        ),
        FinSetMorphism(
            before_edges,
            before_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"B"}),
                frozenset({"AZ"}): frozenset({"Z"}),
                frozenset({"CE"}): frozenset({"E"}),
                frozenset({"DE"}): frozenset({"E"}),
                frozenset({"EF"}): frozenset({"F"}),
                frozenset({"GH1", "GH2"}): frozenset({"H"}),
                frozenset({"GH1", "GH2"}): frozenset({"H"}),
                frozenset({"IJ"}): frozenset({"J"}),
                frozenset({"JK"}): frozenset({"K"}),
            }[e],
        ),
    )

    precondition_map = FinGraphMorphism(
        condition_graph,
        precondition_graph,
        FinSetMorphism(condition_graph.nodes, precondition_graph.nodes, lambda n: n),
        FinSetMorphism(condition_graph.edges, precondition_graph.edges, lambda e: e),
    )
    postcondition_map = FinGraphMorphism(
        condition_graph,
        postcondition_graph,
        FinSetMorphism(condition_graph.nodes, postcondition_graph.nodes, lambda n: n),
        FinSetMorphism(condition_graph.edges, postcondition_graph.edges, lambda e: e),
    )
    match = FinGraphMorphism(
        precondition_graph,
        before_graph,
        FinSetMorphism(
            precondition_graph.nodes,
            before_graph.nodes,
            lambda n: {
                "A": frozenset({"A"}),
                "B": frozenset({"B"}),
                "C": frozenset({"C", "D"}),
                "D": frozenset({"C", "D"}),
                "E": frozenset({"E"}),
                "F": frozenset({"F"}),
                "G": frozenset({"G"}),
                "H": frozenset({"H"}),
                "I": frozenset({"I"}),
                "J": frozenset({"J"}),
                "K": frozenset({"K"}),
                "Z": frozenset({"Z"}),
            }[n],
        ),
        FinSetMorphism(
            precondition_graph.edges,
            before_graph.edges,
            lambda e: {
                "AB": frozenset({"AB"}),
                "AZ": frozenset({"AZ"}),
                "CE": frozenset({"CE"}),
                "DE": frozenset({"DE"}),
                "EF": frozenset({"EF"}),
                "GH1": frozenset({"GH1", "GH2"}),
                "GH2": frozenset({"GH1", "GH2"}),
                "IJ": frozenset({"IJ"}),
                "JK": frozenset({"JK"}),
            }[e],
        ),
    )

    after = double_pushout(
        DoublePushoutRule(precondition_map, postcondition_map),
        before_graph,
        match,
    )

    assert after.nodes == frozenset(
        [
            frozenset({("A", 0), (frozenset({"A"}), 1)}),
            frozenset({("B", 0), (frozenset({"B"}), 1)}),
            frozenset({("C", 0), ("D", 0), (frozenset({"C", "D"}), 1)}),
            frozenset({("E", 0), (frozenset({"E"}), 1)}),
            frozenset({("G", 0), (frozenset({"G"}), 1)}),
            frozenset({("H", 0), (frozenset({"H"}), 1)}),
            frozenset({("I", 0), (frozenset({"I"}), 1)}),
            frozenset({("J", 0), (frozenset({"J"}), 1)}),
            frozenset({("K", 0), (frozenset({"K"}), 1)}),
            frozenset({(frozenset({"Z"}), 1)}),
            frozenset({("L", 0)}),
        ]
    )
    assert after.edges == frozenset(
        [
            frozenset({("AB", 0)}),
            frozenset({(frozenset({"AB"}), 1)}),
            frozenset({(frozenset({"AZ"}), 1)}),
            frozenset({("DE", 0), (frozenset({"DE"}), 1)}),
            frozenset({("GH1", 0), ("GH2", 0), (frozenset({"GH1", "GH2"}), 1)}),
            frozenset({("EL", 0)}),
            frozenset({("IK", 0)}),
        ]
    )
