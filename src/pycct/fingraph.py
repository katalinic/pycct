from dataclasses import dataclass, field
from typing import Dict, Tuple

from .base import (
    Category,
    CoCompleteCategory,
    CoEqualizerCoCone,
    CompleteCategory,
    CoProductCoCone,
    EqualizerCone,
    InitialObject,
    Morphism,
    Object,
    ProductCone,
    Pullback,
    PullbackCone,
    Pushout,
    PushoutCoCone,
    TerminalObject,
)
from .finset import (
    _FST,
    FinSetMorphism,
    FinSetObject,
    finset_coequalizer,
    finset_composition,
    finset_coproduct,
    finset_equalizer,
    finset_identity,
    finset_inclusion,
    finset_product,
    finset_pushout_complement,
    nil_fn,
)


@dataclass(frozen=True, repr=False)
class FinGraphObject(Object):
    nodes: FinSetObject
    edges: FinSetObject
    source: FinSetMorphism
    target: FinSetMorphism
    _source_map: Dict[_FST, _FST] = field(init=False)
    _target_map: Dict[_FST, _FST] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_source_map", {e: self.source(e) for e in self.edges})
        object.__setattr__(self, "_target_map", {e: self.target(e) for e in self.edges})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FinGraphObject):
            raise NotImplementedError()

        return (self.nodes, self.edges, self._source_map, self._target_map) == (
            other.nodes,
            other.edges,
            other._source_map,
            other._target_map,
        )


@dataclass(frozen=True, repr=False)
class FinGraphMorphism(Morphism):
    dom: FinGraphObject
    cod: FinGraphObject
    node_map: FinSetMorphism
    edge_map: FinSetMorphism

    def __post_init__(self) -> None:
        assert self.node_map.dom == self.dom.nodes
        assert self.node_map.cod == self.cod.nodes
        assert self.edge_map.dom == self.dom.edges
        assert self.edge_map.cod == self.cod.edges
        for edge in self.dom.edges:
            mapped_edge = self.edge_map(edge)
            assert self.node_map(self.dom.source(edge)) == self.cod.source(mapped_edge)
            assert self.node_map(self.dom.target(edge)) == self.cod.target(mapped_edge)


def fingraph_source(m: FinGraphMorphism) -> FinGraphObject:
    return m.dom


def fingraph_target(m: FinGraphMorphism) -> FinGraphObject:
    return m.cod


def fingraph_identity(a: FinGraphObject) -> FinGraphMorphism:
    return FinGraphMorphism(a, a, finset_identity(a.nodes), finset_identity(a.edges))


def fingraph_composition(f: FinGraphMorphism, g: FinGraphMorphism) -> FinGraphMorphism:
    return FinGraphMorphism(
        g.dom,
        f.cod,
        finset_composition(f.node_map, g.node_map),
        finset_composition(f.edge_map, g.edge_map),
    )


FinGraphCategory = Category[FinGraphObject, FinGraphMorphism]
FinGraphInitialObject = InitialObject[FinGraphObject, FinGraphMorphism]
FinGraphTerminalObject = TerminalObject[FinGraphObject, FinGraphMorphism]
FinGraphCoProductCoCone = CoProductCoCone[FinGraphObject, FinGraphMorphism]
FinGraphProductCone = ProductCone[FinGraphObject, FinGraphMorphism]
FinGraphCoEqualizerCoCone = CoEqualizerCoCone[FinGraphObject, FinGraphMorphism]
FinGraphEqualizerCone = EqualizerCone[FinGraphObject, FinGraphMorphism]
FinGraphPushoutCoCone = PushoutCoCone[FinGraphObject, FinGraphMorphism]
FinGraphPullbackCone = PullbackCone[FinGraphObject, FinGraphMorphism]

fingraph_category = FinGraphCategory(fingraph_source, fingraph_target, fingraph_identity, fingraph_composition)

fingraph_terminal_obj_obj_value = None
fingraph_terminal_obj_edge_value = (None, None)


fingraph_initial_obj_obj_ = FinSetObject(())
fingraph_initial_obj_edge_ = FinSetObject(())


fingraph_initial_obj_ = FinGraphObject(
    fingraph_initial_obj_obj_,
    fingraph_initial_obj_edge_,
    FinSetMorphism(fingraph_initial_obj_edge_, fingraph_initial_obj_obj_, nil_fn),
    FinSetMorphism(fingraph_initial_obj_edge_, fingraph_initial_obj_obj_, nil_fn),
)


def fingraph_initial_obj_univ_obj_proj(a: _FST) -> _FST:
    raise NotImplementedError()


def fingraph_initial_obj_univ_edge_proj(a: _FST) -> _FST:
    raise NotImplementedError()


def fingraph_initial_obj_univ(a: FinGraphObject) -> FinGraphMorphism:
    return FinGraphMorphism(
        fingraph_initial_obj_,
        a,
        FinSetMorphism(fingraph_initial_obj_obj_, a.nodes, fingraph_initial_obj_univ_obj_proj),
        FinSetMorphism(fingraph_initial_obj_edge_, a.edges, fingraph_initial_obj_univ_edge_proj),
    )


fingraph_initial_obj = FinGraphInitialObject(fingraph_initial_obj_, fingraph_initial_obj_univ)


fingraph_terminal_obj_obj_ = FinSetObject((fingraph_terminal_obj_obj_value,))
fingraph_terminal_obj_edge_ = FinSetObject((fingraph_terminal_obj_edge_value,))


def fingraph_terminal_obj_edge_source(a: _FST) -> _FST:
    return fingraph_terminal_obj_obj_value


def fingraph_terminal_obj_edge_target(a: _FST) -> _FST:
    return fingraph_terminal_obj_obj_value


fingraph_terminal_obj_ = FinGraphObject(
    fingraph_terminal_obj_obj_,
    fingraph_terminal_obj_edge_,
    FinSetMorphism(fingraph_terminal_obj_edge_, fingraph_terminal_obj_obj_, fingraph_terminal_obj_edge_source),
    FinSetMorphism(fingraph_terminal_obj_edge_, fingraph_terminal_obj_obj_, fingraph_terminal_obj_edge_target),
)


def fingraph_terminal_obj_univ_obj_proj(a: _FST) -> _FST:
    return fingraph_terminal_obj_obj_value


def fingraph_terminal_obj_univ_edge_proj(a: _FST) -> _FST:
    return fingraph_terminal_obj_edge_value


def fingraph_terminal_obj_univ(a: FinGraphObject) -> FinGraphMorphism:
    return FinGraphMorphism(
        a,
        fingraph_terminal_obj_,
        FinSetMorphism(a.nodes, fingraph_terminal_obj_obj_, fingraph_terminal_obj_univ_obj_proj),
        FinSetMorphism(a.edges, fingraph_terminal_obj_edge_, fingraph_terminal_obj_univ_edge_proj),
    )


fingraph_terminal_obj = FinGraphTerminalObject(fingraph_terminal_obj_, fingraph_terminal_obj_univ)


def fingraph_coproduct(a: FinGraphObject, b: FinGraphObject) -> FinGraphCoProductCoCone:
    disjoint_union_node_coprod = finset_coproduct(a.nodes, b.nodes)
    disjoint_union_edge_coprod = finset_coproduct(a.edges, b.edges)

    disjoint_union_nodes: FinSetObject = disjoint_union_node_coprod.apex
    disjoint_union_edges: FinSetObject = disjoint_union_edge_coprod.apex

    def disjoint_union_edge_source(x: _FST) -> _FST:
        return (a.source(x[0]), 0) if x[1] == 0 else (b.source(x[0]), 1)  # type: ignore

    def disjoint_union_edge_target(x: _FST) -> _FST:
        return (a.target(x[0]), 0) if x[1] == 0 else (b.target(x[0]), 1)  # type: ignore

    disjoint_union = FinGraphObject(
        disjoint_union_nodes,
        disjoint_union_edges,
        FinSetMorphism(disjoint_union_edges, disjoint_union_nodes, disjoint_union_edge_source),
        FinSetMorphism(disjoint_union_edges, disjoint_union_nodes, disjoint_union_edge_target),
    )

    def fingraph_coproduct_univ(p: FinGraphMorphism, q: FinGraphMorphism) -> FinGraphMorphism:
        assert p.cod == q.cod
        assert p.dom == a and q.dom == b
        return FinGraphMorphism(
            disjoint_union,
            p.cod,
            disjoint_union_node_coprod.univ(p.node_map, q.node_map),
            disjoint_union_edge_coprod.univ(p.edge_map, q.edge_map),
        )

    return FinGraphCoProductCoCone(
        disjoint_union,
        FinGraphMorphism(a, disjoint_union, disjoint_union_node_coprod.proj_a, disjoint_union_edge_coprod.proj_a),
        FinGraphMorphism(b, disjoint_union, disjoint_union_node_coprod.proj_b, disjoint_union_edge_coprod.proj_b),
        fingraph_coproduct_univ,
    )


def fingraph_product(a: FinGraphObject, b: FinGraphObject) -> FinGraphProductCone:
    cartesian_product_node_prod = finset_product(a.nodes, b.nodes)
    cartesian_product_edge_prod = finset_product(a.edges, b.edges)

    cartesian_product_nodes: FinSetObject = cartesian_product_node_prod.apex
    cartesian_product_edges: FinSetObject = cartesian_product_edge_prod.apex

    def cartesian_product_edge_source(x: _FST) -> _FST:
        return (a.source(x[0]), b.source(x[1]))  # type: ignore

    def cartesian_product_edge_target(x: _FST) -> _FST:
        return (a.target(x[0]), b.target(x[1]))  # type: ignore

    cartesian_product = FinGraphObject(
        cartesian_product_nodes,
        cartesian_product_edges,
        FinSetMorphism(cartesian_product_edges, cartesian_product_nodes, cartesian_product_edge_source),
        FinSetMorphism(cartesian_product_edges, cartesian_product_nodes, cartesian_product_edge_target),
    )

    def fingraph_product_univ(p: FinGraphMorphism, q: FinGraphMorphism) -> FinGraphMorphism:
        assert p.dom == q.dom
        assert p.cod == a and q.cod == b
        return FinGraphMorphism(
            p.dom,
            cartesian_product,
            cartesian_product_node_prod.univ(p.node_map, q.node_map),
            cartesian_product_edge_prod.univ(p.edge_map, q.edge_map),
        )

    return FinGraphProductCone(
        cartesian_product,
        FinGraphMorphism(cartesian_product, a, cartesian_product_node_prod.proj_a, cartesian_product_edge_prod.proj_a),
        FinGraphMorphism(cartesian_product, b, cartesian_product_node_prod.proj_b, cartesian_product_edge_prod.proj_b),
        fingraph_product_univ,
    )


def fingraph_coequalizer(f: FinGraphMorphism, g: FinGraphMorphism) -> FinGraphCoEqualizerCoCone:
    assert f.dom == g.dom and f.cod == g.cod

    node_coeq = finset_coequalizer(f.node_map, g.node_map)
    edge_coeq = finset_coequalizer(f.edge_map, g.edge_map)

    edge_src = edge_coeq.univ(finset_composition(node_coeq.proj, f.cod.source))
    edge_tgt = edge_coeq.univ(finset_composition(node_coeq.proj, f.cod.target))

    coeq = FinGraphObject(edge_src.cod, edge_src.dom, edge_src, edge_tgt)
    coeq_proj = FinGraphMorphism(f.cod, coeq, node_coeq.proj, edge_coeq.proj)

    def fingraph_coequalizer_univ(q: FinGraphMorphism) -> FinGraphMorphism:
        assert q.dom == f.cod
        return FinGraphMorphism(coeq, q.cod, node_coeq.univ(q.node_map), edge_coeq.univ(q.edge_map))

    return FinGraphCoEqualizerCoCone(coeq, coeq_proj, fingraph_coequalizer_univ)


def fingraph_equalizer(f: FinGraphMorphism, g: FinGraphMorphism) -> FinGraphEqualizerCone:
    assert f.dom == g.dom

    node_eq = finset_equalizer(f.node_map, g.node_map)
    edge_eq = finset_equalizer(f.edge_map, g.edge_map)

    eq = FinGraphObject(
        node_eq.apex,
        edge_eq.apex,
        finset_composition(f.dom.source, edge_eq.proj),
        finset_composition(f.dom.target, edge_eq.proj),
    )
    eq_proj = FinGraphMorphism(eq, f.dom, node_eq.proj, edge_eq.proj)

    def fingraph_equalizer_univ(p: FinGraphMorphism) -> FinGraphMorphism:
        assert p.cod == f.dom
        return FinGraphMorphism(p.dom, eq, node_eq.univ(p.node_map), edge_eq.univ(p.edge_map))

    return FinGraphEqualizerCone(eq, eq_proj, fingraph_equalizer_univ)


FinGraphCoComplete = CoCompleteCategory[FinGraphObject, FinGraphMorphism]
FinGraphComplete = CompleteCategory[FinGraphObject, FinGraphMorphism]

fingraph_cocomplete = FinGraphCoComplete(fingraph_category, fingraph_coproduct, fingraph_coequalizer)
fingraph_complete = FinGraphComplete(fingraph_category, fingraph_product, fingraph_equalizer)

FinGraphPushout = Pushout[FinGraphMorphism, FinGraphObject]
FinGraphPullback = Pullback[FinGraphMorphism, FinGraphObject]


def fingraph_pushout(f: FinGraphMorphism, g: FinGraphMorphism) -> FinGraphPushoutCoCone:
    assert f.dom == g.dom
    cp = fingraph_coproduct(f.cod, g.cod)
    ce = fingraph_coequalizer(fingraph_composition(cp.proj_a, f), fingraph_composition(cp.proj_b, g))

    def fingraph_pushout_univ(u: FinGraphMorphism, v: FinGraphMorphism) -> FinGraphMorphism:
        assert u.cod == v.cod
        assert u.dom == f.cod and v.dom == g.cod
        return ce.univ(cp.univ(u, v))

    return FinGraphPushoutCoCone(
        ce.apex,
        fingraph_composition(ce.proj, cp.proj_a),
        fingraph_composition(ce.proj, cp.proj_b),
        fingraph_pushout_univ,
    )


def fingraph_pullback(f: FinGraphMorphism, g: FinGraphMorphism) -> FinGraphPullbackCone:
    assert f.cod == g.cod
    p = fingraph_product(f.dom, g.dom)
    e = fingraph_equalizer(fingraph_composition(f, p.proj_a), fingraph_composition(g, p.proj_b))

    def fingraph_pullback_univ(u: FinGraphMorphism, v: FinGraphMorphism) -> FinGraphMorphism:
        assert u.dom == v.dom
        assert u.cod == f.dom and v.cod == g.dom
        return e.univ(p.univ(u, v))

    return FinGraphPullbackCone(
        e.apex, fingraph_composition(p.proj_a, e.proj), fingraph_composition(p.proj_b, e.proj), fingraph_pullback_univ
    )


def fingraph_pushout_complement(
    f_or_g: FinGraphMorphism, proj_b_or_c: FinGraphMorphism, pushout_apex: FinGraphObject
) -> Tuple[FinGraphObject, FinGraphMorphism, FinGraphMorphism]:
    assert f_or_g.cod == proj_b_or_c.dom
    assert proj_b_or_c.cod == pushout_apex

    node_complement, node_g_or_f, node_proj_c_or_b = finset_pushout_complement(
        f_or_g.node_map, proj_b_or_c.node_map, pushout_apex.nodes
    )
    edge_complement, edge_g_or_f, edge_proj_c_or_b = finset_pushout_complement(
        f_or_g.edge_map, proj_b_or_c.edge_map, pushout_apex.edges
    )
    complement = FinGraphObject(
        node_complement,
        edge_complement,
        finset_composition(pushout_apex.source, edge_proj_c_or_b),
        finset_composition(pushout_apex.target, edge_proj_c_or_b),
    )

    # Dangling condition.
    deleted_nodes = pushout_apex.nodes - node_complement
    for edge in pushout_apex.edges:
        if pushout_apex.source(edge) in deleted_nodes or pushout_apex.target(edge) in deleted_nodes:
            assert edge not in edge_complement
    # Identification condition satisfied by assumed injectivity.

    g_or_f = FinGraphMorphism(f_or_g.dom, complement, node_g_or_f, edge_g_or_f)
    proj_c_or_b = FinGraphMorphism(complement, pushout_apex, node_proj_c_or_b, edge_proj_c_or_b)

    return complement, g_or_f, proj_c_or_b


def fingraph_inclusion(a: FinGraphObject, b: FinGraphObject) -> FinGraphMorphism:
    return FinGraphMorphism(a, b, finset_inclusion(a.nodes, b.nodes), finset_inclusion(a.edges, b.edges))
