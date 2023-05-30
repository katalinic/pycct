import sys
from typing import Tuple

from pycct import _FST, FinGraphMorphism, FinGraphObject, FinSetMorphism, fingraph_inclusion

from .lsa import SUCCESSOR_EDGE_FMT, SUCCESSOR_NODE_FMT, lsa, peano_tree_to_str, str_to_peano_tree


def increment_last_char_horizontal_peano_subgraph(
    a_graph: FinGraphObject, b_graph: FinGraphObject
) -> Tuple[FinGraphObject, FinGraphMorphism, FinGraphMorphism]:
    a = peano_tree_to_str(a_graph)
    peano_tree_to_str(b_graph)

    common = str_to_peano_tree(a)
    common = FinGraphObject(
        common.nodes,
        common.edges - frozenset({SUCCESSOR_EDGE_FMT.format(len(a) - 1, 0, 1)}),
        common.source,
        common.target,
    )

    def node_map_a(n: _FST) -> _FST:
        node_split = n.split("_")
        if node_split[0] == SUCCESSOR_NODE_FMT[0] and int(node_split[1]) == len(a) - 1:
            return SUCCESSOR_NODE_FMT.format(node_split[1], int(node_split[2]))

        return n

    def edge_map_a(e: _FST) -> _FST:
        edge_split = e.split("_")
        if edge_split[0] == SUCCESSOR_EDGE_FMT[0] and int(edge_split[1]) == len(a) - 1:
            return SUCCESSOR_EDGE_FMT.format(edge_split[1], int(edge_split[2]), int(edge_split[3]))

        return e

    def node_map_b(n: _FST) -> _FST:
        node_split = n.split("_")
        if node_split[0] == SUCCESSOR_NODE_FMT[0] and int(node_split[1]) == len(a) - 1:
            return SUCCESSOR_NODE_FMT.format(node_split[1], int(node_split[2]) + 1)

        return n

    def edge_map_b(e: _FST) -> _FST:
        edge_split = e.split("_")
        if edge_split[0] == SUCCESSOR_EDGE_FMT[0] and int(edge_split[1]) == len(a) - 1:
            return SUCCESSOR_EDGE_FMT.format(edge_split[1], int(edge_split[2]) + 1, int(edge_split[3]) + 1)

        return e

    common_to_a = FinGraphMorphism(
        common,
        a_graph,
        node_map=FinSetMorphism(common.nodes, a_graph.nodes, node_map_a),
        edge_map=FinSetMorphism(common.edges, a_graph.edges, edge_map_a),
    )
    common_to_b = FinGraphMorphism(
        common,
        b_graph,
        node_map=FinSetMorphism(common.nodes, b_graph.nodes, node_map_b),
        edge_map=FinSetMorphism(common.edges, b_graph.edges, edge_map_b),
    )

    return common, common_to_a, common_to_b


def increment_last_char_vertical_peano_subgraph(
    a_graph: FinGraphObject, b_graph: FinGraphObject
) -> Tuple[FinGraphObject, FinGraphMorphism, FinGraphMorphism]:
    num_chars = len([a for a in a_graph.nodes if a.startswith("C")])
    common = str_to_peano_tree("a" * (num_chars - 1) + "b")
    return common, fingraph_inclusion(common, a_graph), fingraph_inclusion(common, b_graph)


def lsa_increment_last(a: str, b: str, c: str) -> str:
    assert len(a) >= 3 and len(b) >= 3 and len(c) >= 3
    assert len(a) == len(b) == len(c)
    assert all(x == y for x, y in zip(a[:-1], b[:-1]))
    assert ord(b[-1]) == ord(a[-1]) + 1
    return lsa(a, b, c, increment_last_char_horizontal_peano_subgraph, increment_last_char_vertical_peano_subgraph)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("Please call this as `python3 main.py arg1 arg2 arg3`.")

    _, a, b, c = sys.argv
    print(f"{a} is to {b} as {c} is to {lsa_increment_last(a, b, c)}.")
