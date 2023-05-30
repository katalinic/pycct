from collections import defaultdict
from typing import Callable, Tuple

from pycct import (
    _FST,
    DoublePushoutRule,
    FinGraphMorphism,
    FinGraphObject,
    FinSetMorphism,
    FinSetObject,
    double_pushout,
    fingraph_pullback,
    fingraph_pushout_complement,
)


BEGIN_NODE_FMT = "C_{0}"
BEGIN_EDGE_FMT = "C_{0}_{1}"
SUCCESSOR_NODE_FMT = "S_{0}_{1}"
SUCCESSOR_EDGE_FMT = "S_{0}_{1}_{2}"


def edge_source(e: _FST) -> _FST:
    edge_parts = e.split("_")
    if edge_parts[0] == BEGIN_NODE_FMT[0]:
        # B_x_y -> B_x
        return BEGIN_NODE_FMT.format(edge_parts[1])
    elif edge_parts[0] == SUCCESSOR_NODE_FMT[0]:
        # S_x_y_z
        if edge_parts[2] == "0":
            # S_x_0_z -> B_x
            return BEGIN_NODE_FMT.format(edge_parts[1])
        else:
            # S_x_y_z -> S_x_y
            return SUCCESSOR_NODE_FMT.format(edge_parts[1], edge_parts[2])
    else:
        raise Exception


def edge_target(e: _FST) -> _FST:
    edge_parts = e.split("_")
    if edge_parts[0] == BEGIN_NODE_FMT[0]:
        # B_x_y -> B_y
        return BEGIN_NODE_FMT.format(edge_parts[2])
    elif edge_parts[0] == SUCCESSOR_NODE_FMT[0]:
        # S_x_y_z -> S_x_z
        return SUCCESSOR_NODE_FMT.format(edge_parts[1], edge_parts[3])
    else:
        raise Exception


def str_to_peano_tree(x: str) -> FinGraphObject:
    nodes = []
    edges = []

    prev = None
    for i, char in enumerate(x):
        begin_node = BEGIN_NODE_FMT.format(i)
        nodes.append(begin_node)
        if prev is not None:
            edge = BEGIN_EDGE_FMT.format(i - 1, i)
            edges.append(edge)
        prev = begin_node

        num_successors = ord(str.lower(char)) - ord("a")
        for j in range(1, num_successors + 1):
            node = SUCCESSOR_NODE_FMT.format(i, j)
            edge = SUCCESSOR_EDGE_FMT.format(i, 0 if j == 1 else j - 1, j)
            nodes.append(node)
            edges.append(edge)

    nodes_obj = FinSetObject(nodes)
    edges_obj = FinSetObject(edges)
    return FinGraphObject(
        nodes_obj,
        edges_obj,
        FinSetMorphism(edges_obj, nodes_obj, edge_source),
        FinSetMorphism(edges_obj, nodes_obj, edge_target),
    )


def peano_tree_to_str(x: FinGraphObject) -> str:
    num_chars = len([a for a in x.nodes if a.startswith("C")])

    grouped_nodes = defaultdict(list)
    for node in x.nodes:
        node_split = node.split("_")
        if node_split[0] != "S":
            continue

        grouped_nodes[int(node_split[1])].append(node)

    chars = []
    for i in range(num_chars):
        num_successors = len(grouped_nodes[i])
        chars.append(chr(ord("a") + num_successors))

    return "".join(chars)


def lsa(
    a: str,
    b: str,
    c: str,
    infer_a_b_common_subgraph: Callable[
        [FinGraphObject, FinGraphObject], Tuple[FinGraphObject, FinGraphMorphism, FinGraphMorphism]
    ],
    infer_a_c_common_subgraph: Callable[
        [FinGraphObject, FinGraphObject], Tuple[FinGraphObject, FinGraphMorphism, FinGraphMorphism]
    ],
) -> str:
    a_graph = str_to_peano_tree(a)
    b_graph = str_to_peano_tree(b)
    c_graph = str_to_peano_tree(c)

    # The common subgraphs completely determine the transformation.
    _, ab_common_to_a_map, ab_common_to_b_map = infer_a_b_common_subgraph(a_graph, b_graph)
    _, ac_common_to_a_map, ac_common_to_c_map = infer_a_c_common_subgraph(a_graph, c_graph)

    condition_pullback = fingraph_pullback(ab_common_to_a_map, ac_common_to_a_map)
    _, precondition_map = condition_pullback.apex, condition_pullback.proj_c
    _, postcondition_map, _ = fingraph_pushout_complement(condition_pullback.proj_b, ab_common_to_b_map, b_graph)
    d_graph = double_pushout(
        DoublePushoutRule(precondition_map, postcondition_map),
        c_graph,
        ac_common_to_c_map,
    )

    successor_counts = [0] * len(a)
    for pushout_node in d_graph.nodes:
        node_split = next(iter(pushout_node))[0].split("_")
        if node_split[0] == "S":
            successor_counts[int(node_split[1])] += 1

    d = "".join(chr(ord("a") + successor_count) for successor_count in successor_counts)
    return d
