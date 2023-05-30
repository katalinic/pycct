import pytest
from pycct import (
    FinGraphMorphism,
    FinGraphObject,
    FinSetMorphism,
    FinSetObject,
    fingraph_coequalizer,
    fingraph_coproduct,
    fingraph_equalizer,
    fingraph_product,
    fingraph_pullback,
    fingraph_pushout,
    fingraph_pushout_complement,
    finset_composition,
)


def test_coproduct():
    a_nodes = FinSetObject(["A", "B", "C"])
    a_edges = FinSetObject(["E", "F"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda _: "A"),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"E": "B", "F": "C"}[e]),
    )
    b_nodes = FinSetObject(["S", "T"])
    b_edges = FinSetObject(["U"])
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda _: "S"),
        FinSetMorphism(b_edges, b_nodes, lambda _: "T"),
    )

    coproduct = fingraph_coproduct(a_graph, b_graph)
    assert coproduct.apex.nodes == frozenset([("A", 0), ("B", 0), ("C", 0), ("S", 1), ("T", 1)])
    assert coproduct.apex.edges == frozenset([("E", 0), ("F", 0), ("U", 1)])
    assert (
        frozenset(map(coproduct.proj_a.node_map, a_graph.nodes)).union(
            frozenset(map(coproduct.proj_b.node_map, b_graph.nodes))
        )
        == coproduct.apex.nodes
    )
    assert (
        frozenset(map(coproduct.proj_a.edge_map, a_graph.edges)).union(
            frozenset(map(coproduct.proj_b.edge_map, b_graph.edges))
        )
        == coproduct.apex.edges
    )


def test_product():
    a_nodes = FinSetObject(["A", "B", "C"])
    a_edges = FinSetObject(["E", "F"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda _: "A"),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"E": "B", "F": "C"}[e]),
    )
    b_nodes = FinSetObject(["S", "T"])
    b_edges = FinSetObject(["U"])
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda _: "S"),
        FinSetMorphism(b_edges, b_nodes, lambda _: "T"),
    )

    product = fingraph_product(a_graph, b_graph)
    assert product.apex.nodes == frozenset([("A", "S"), ("A", "T"), ("B", "S"), ("B", "T"), ("C", "S"), ("C", "T")])
    assert product.apex.edges == frozenset([("E", "U"), ("F", "U")])
    assert frozenset(map(product.proj_a.node_map, product.apex.nodes)) == a_graph.nodes
    assert frozenset(map(product.proj_a.edge_map, product.apex.edges)) == a_graph.edges
    assert frozenset(map(product.proj_b.node_map, product.apex.nodes)) == b_graph.nodes
    assert frozenset(map(product.proj_b.edge_map, product.apex.edges)) == b_graph.edges


def test_coequalizer():
    a_nodes = FinSetObject(["A", "B", "C"])
    a_edges = FinSetObject(["E", "F"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda _: "A"),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"E": "B", "F": "C"}[e]),
    )
    b_nodes = FinSetObject(["R", "S", "T", "Q"])
    b_edges = FinSetObject(["U", "V", "W"])
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda _: "R"),
        FinSetMorphism(b_edges, b_nodes, lambda e: {"U": "S", "V": "T", "W": "Q"}[e]),
    )

    f = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: {"A": "R", "B": "S", "C": "T"}[n]),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: {"E": "U", "F": "V"}[e]),
    )
    g = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: {"A": "R", "B": "Q", "C": "T"}[n]),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: {"E": "W", "F": "V"}[e]),
    )

    coequalizer = fingraph_coequalizer(f, g)
    assert coequalizer.apex.nodes == frozenset(
        [
            frozenset({"R"}),
            frozenset({"T"}),
            frozenset({"S", "Q"}),
        ]
    )
    assert coequalizer.apex.edges == frozenset(
        [
            frozenset({"W", "U"}),
            frozenset({"V"}),
        ]
    )


def test_equalizer():
    a_nodes = FinSetObject(["A", "B", "C"])
    a_edges = FinSetObject(["E", "F"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda _: "A"),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"E": "B", "F": "C"}[e]),
    )
    b_nodes = FinSetObject(["R", "S", "T"])
    b_edges = FinSetObject(["U", "V"])
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda _: "R"),
        FinSetMorphism(b_edges, b_nodes, lambda e: {"U": "S", "V": "T"}[e]),
    )

    f = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: {"A": "R", "B": "S", "C": "S"}[n]),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: {"E": "U", "F": "U"}[e]),
    )
    g = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: {"A": "R", "B": "S", "C": "T"}[n]),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: {"E": "U", "F": "V"}[e]),
    )

    equalizer = fingraph_equalizer(f, g)
    assert equalizer.apex.nodes == frozenset(["A", "B"])
    assert equalizer.apex.edges == frozenset(["E"])


def test_pushout():
    a_nodes = FinSetObject(["A", "B", "C"])
    a_edges = FinSetObject(["E", "F"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda _: "B"),
        FinSetMorphism(a_edges, a_nodes, lambda E: "A" if E == "E" else "C"),
    )
    b_nodes = FinSetObject(["A", "B", "C", "D"])
    b_edges = FinSetObject(["E", "F", "G", "H"])
    b_target_dict = {"E": "A", "F": "C", "G": "C", "H": "D"}
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda e: "A" if e == "G" else "B"),
        FinSetMorphism(b_edges, b_nodes, lambda e: b_target_dict[e]),
    )
    c_nodes = FinSetObject(["A", "B", "D"])
    c_edges = FinSetObject(["F", "G", "H"])
    c_graph = FinGraphObject(
        c_nodes,
        c_edges,
        FinSetMorphism(c_edges, c_nodes, lambda e: "B" if e == "H" else "A"),
        FinSetMorphism(c_edges, c_nodes, lambda e: "B" if e == "F" else "D"),
    )

    f = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda x: x),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda x: x),
    )
    g = FinGraphMorphism(
        a_graph,
        c_graph,
        FinSetMorphism(a_graph.nodes, c_graph.nodes, lambda n: "A" if n == "B" else "B"),
        FinSetMorphism(a_graph.edges, c_graph.edges, lambda _: "F"),
    )

    pushout = fingraph_pushout(f, g)
    assert pushout.apex.nodes == frozenset(
        [
            frozenset({("D", 1)}),
            frozenset({("D", 0)}),
            frozenset({("B", 0), ("A", 1)}),
            frozenset({("C", 0), ("B", 1), ("A", 0)}),
        ]
    )
    assert pushout.apex.edges == frozenset(
        [
            frozenset({("G", 0)}),
            frozenset({("G", 1)}),
            frozenset({("E", 0), ("F", 0), ("F", 1)}),
            frozenset({("H", 0)}),
            frozenset({("H", 1)}),
        ]
    )


def test_pullback():
    a_nodes = FinSetObject(["A", "B", "D"])
    a_edges = FinSetObject(["F", "G", "H"])
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda e: "B" if e == "H" else "A"),
        FinSetMorphism(a_edges, a_nodes, lambda e: "B" if e == "F" else "D"),
    )
    b_nodes = FinSetObject(["A", "B", "C", "D"])
    b_edges = FinSetObject(["E", "F", "G", "H"])
    b_target_dict = {"E": "A", "F": "C", "G": "C", "H": "D"}
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(b_edges, b_nodes, lambda e: "A" if e == "G" else "B"),
        FinSetMorphism(b_edges, b_nodes, lambda e: b_target_dict[e]),
    )
    c_nodes = FinSetObject(["A", "B", "C"])
    c_edges = FinSetObject(["E", "F"])
    c_graph = FinGraphObject(
        c_nodes,
        c_edges,
        FinSetMorphism(c_edges, c_nodes, lambda _: "B"),
        FinSetMorphism(c_edges, c_nodes, lambda e: "A" if e == "E" else "C"),
    )

    f_node_dict = {"B": "A", "A": "B", "C": "D", "D": "D"}
    f_edge_dict = {"E": "F", "F": "G", "G": "H", "H": "G"}
    f = FinGraphMorphism(
        b_graph,
        a_graph,
        FinSetMorphism(b_graph.nodes, a_graph.nodes, lambda n: f_node_dict[n]),
        FinSetMorphism(b_graph.edges, a_graph.edges, lambda e: f_edge_dict[e]),
    )
    g_node_dict = {"B": "A", "A": "B", "C": "D"}
    g_edge_dict = {"E": "F", "F": "G"}
    g = FinGraphMorphism(
        c_graph,
        a_graph,
        FinSetMorphism(c_graph.nodes, a_graph.nodes, lambda n: g_node_dict[n]),
        FinSetMorphism(c_graph.edges, a_graph.edges, lambda e: g_edge_dict[e]),
    )

    pullback = fingraph_pullback(f, g)
    assert pullback.apex.nodes == frozenset([("D", "C"), ("B", "B"), ("A", "A"), ("C", "C")])
    assert pullback.apex.edges == frozenset([("F", "F"), ("H", "F"), ("E", "E")])


def test_fingraph_pushout_complement():
    a_nodes = FinSetObject(["A", "B", "C", "D", "E", "G", "H", "I", "J", "K"])
    b_nodes = FinSetObject(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
    d_nodes = FinSetObject(
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
    a_edges = FinSetObject(["DE", "GH1", "GH2"])
    b_edges = FinSetObject(["CE", "DE", "EF", "GH1", "GH2", "IJ", "JK"])
    d_edges = FinSetObject(
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
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda e: {"DE": "D", "GH1": "G", "GH2": "G"}[e]),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"DE": "E", "GH1": "H", "GH2": "H"}[e]),
    )
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(
            b_edges,
            b_nodes,
            lambda e: {"CE": "C", "DE": "D", "EF": "E", "GH1": "G", "GH2": "G", "IJ": "I", "JK": "J"}[e],
        ),
        FinSetMorphism(
            b_edges,
            b_nodes,
            lambda e: {"CE": "E", "DE": "E", "EF": "F", "GH1": "H", "GH2": "H", "IJ": "J", "JK": "K"}[e],
        ),
    )
    d_graph = FinGraphObject(
        d_nodes,
        d_edges,
        FinSetMorphism(
            d_edges,
            d_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"A"}),
                frozenset({"AZ"}): frozenset({"A"}),
                frozenset({"CE"}): frozenset({"C", "D"}),
                frozenset({"DE"}): frozenset({"C", "D"}),
                frozenset({"EF"}): frozenset({"E"}),
                frozenset({"GH1", "GH2"}): frozenset({"G"}),
                frozenset({"IJ"}): frozenset({"I"}),
                frozenset({"JK"}): frozenset({"J"}),
            }[e],
        ),
        FinSetMorphism(
            d_edges,
            d_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"B"}),
                frozenset({"AZ"}): frozenset({"Z"}),
                frozenset({"CE"}): frozenset({"E"}),
                frozenset({"DE"}): frozenset({"E"}),
                frozenset({"EF"}): frozenset({"F"}),
                frozenset({"GH1", "GH2"}): frozenset({"H"}),
                frozenset({"IJ"}): frozenset({"J"}),
                frozenset({"JK"}): frozenset({"K"}),
            }[e],
        ),
    )

    f = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: n),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: e),
    )
    proj_b = FinGraphMorphism(
        b_graph,
        d_graph,
        FinSetMorphism(
            b_graph.nodes,
            d_graph.nodes,
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
            b_graph.edges,
            d_graph.edges,
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

    complement, g, proj_c = fingraph_pushout_complement(f, proj_b, d_graph)

    assert complement.nodes == frozenset(
        [
            frozenset({"A"}),
            frozenset({"B"}),
            frozenset({"C", "D"}),
            frozenset({"E"}),
            frozenset({"G"}),
            frozenset({"H"}),
            frozenset({"I"}),
            frozenset({"J"}),
            frozenset({"K"}),
            frozenset({"Z"}),
        ]
    )
    assert complement.edges == frozenset(
        [
            frozenset({"AB"}),
            frozenset({"AZ"}),
            frozenset({"DE"}),
            frozenset({"GH1", "GH2"}),
        ]
    )
    assert frozenset(map(g.node_map, a_graph.nodes)).issubset(complement.nodes)
    assert frozenset(map(g.edge_map, a_graph.edges)).issubset(complement.edges)
    assert frozenset(map(proj_c.node_map, complement.nodes)).issubset(d_graph.nodes)
    assert frozenset(map(proj_c.edge_map, complement.edges)).issubset(d_graph.edges)
    assert all(
        finset_composition(proj_c.node_map, g.node_map)(x) == finset_composition(proj_b.node_map, f.node_map)(x)
        for x in a_graph.nodes
    )
    assert all(
        finset_composition(proj_c.edge_map, g.edge_map)(x) == finset_composition(proj_b.edge_map, f.edge_map)(x)
        for x in a_graph.edges
    )


def test_fingraph_pushout_complement_no_gluing():
    a_nodes = FinSetObject(["B", "C", "D", "E", "G", "H", "I", "J", "K"])
    b_nodes = FinSetObject(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
    d_nodes = FinSetObject(
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
    a_edges = FinSetObject(["DE", "GH1", "GH2"])
    b_edges = FinSetObject(["CE", "DE", "EF", "GH1", "GH2", "IJ", "JK"])
    d_edges = FinSetObject(
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
    a_graph = FinGraphObject(
        a_nodes,
        a_edges,
        FinSetMorphism(a_edges, a_nodes, lambda e: {"DE": "D", "GH1": "G", "GH2": "G"}[e]),
        FinSetMorphism(a_edges, a_nodes, lambda e: {"DE": "E", "GH1": "H", "GH2": "H"}[e]),
    )
    b_graph = FinGraphObject(
        b_nodes,
        b_edges,
        FinSetMorphism(
            b_edges,
            b_nodes,
            lambda e: {"CE": "C", "DE": "D", "EF": "E", "GH1": "G", "GH2": "G", "IJ": "I", "JK": "J"}[e],
        ),
        FinSetMorphism(
            b_edges,
            b_nodes,
            lambda e: {"CE": "E", "DE": "E", "EF": "F", "GH1": "H", "GH2": "H", "IJ": "J", "JK": "K"}[e],
        ),
    )
    d_graph = FinGraphObject(
        d_nodes,
        d_edges,
        FinSetMorphism(
            d_edges,
            d_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"A"}),
                frozenset({"AZ"}): frozenset({"A"}),
                frozenset({"CE"}): frozenset({"C", "D"}),
                frozenset({"DE"}): frozenset({"C", "D"}),
                frozenset({"EF"}): frozenset({"E"}),
                frozenset({"GH1", "GH2"}): frozenset({"G"}),
                frozenset({"IJ"}): frozenset({"I"}),
                frozenset({"JK"}): frozenset({"J"}),
            }[e],
        ),
        FinSetMorphism(
            d_edges,
            d_nodes,
            lambda e: {
                frozenset({"AB"}): frozenset({"B"}),
                frozenset({"AZ"}): frozenset({"Z"}),
                frozenset({"CE"}): frozenset({"E"}),
                frozenset({"DE"}): frozenset({"E"}),
                frozenset({"EF"}): frozenset({"F"}),
                frozenset({"GH1", "GH2"}): frozenset({"H"}),
                frozenset({"IJ"}): frozenset({"J"}),
                frozenset({"JK"}): frozenset({"K"}),
            }[e],
        ),
    )

    f = FinGraphMorphism(
        a_graph,
        b_graph,
        FinSetMorphism(a_graph.nodes, b_graph.nodes, lambda n: n),
        FinSetMorphism(a_graph.edges, b_graph.edges, lambda e: e),
    )
    proj_b = FinGraphMorphism(
        b_graph,
        d_graph,
        FinSetMorphism(
            b_graph.nodes,
            d_graph.nodes,
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
            b_graph.edges,
            d_graph.edges,
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

    with pytest.raises(AssertionError):
        fingraph_pushout_complement(f, proj_b, d_graph)
