from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Callable, Dict, Hashable, Iterable, List, Tuple

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


_FST = Hashable


def nil_fn(a: _FST) -> _FST:
    raise NotImplementedError()


class FinSetObject(frozenset[_FST], Object):
    pass


@dataclass(frozen=True, repr=False)
class FinSetMorphism(Morphism):
    dom: FinSetObject
    cod: FinSetObject
    value: Callable[[_FST], _FST]

    def __post_init__(self) -> None:
        assert frozenset(map(self, self.dom)).issubset(self.cod)

    def __call__(self, x: _FST) -> _FST:
        return self.value(x)


def is_injective(f: FinSetMorphism) -> bool:
    return len(f.dom) == len(set(map(f, f.dom)))


def finset_source(m: FinSetMorphism) -> FinSetObject:
    return m.dom


def finset_target(m: FinSetMorphism) -> FinSetObject:
    return m.cod


def finset_identity(a: FinSetObject) -> FinSetMorphism:
    def finset_id_(x: _FST) -> _FST:
        return x

    return FinSetMorphism(a, a, finset_id_)


def finset_composition(f: FinSetMorphism, g: FinSetMorphism) -> FinSetMorphism:
    if f.dom != g.cod:
        raise ValueError(f"Composition of {f} * {g} failed with: {f.dom=} != {g.cod=}.")

    def finset_comp_(x: _FST) -> _FST:
        return f(g(x))

    return FinSetMorphism(g.dom, f.cod, finset_comp_)


FinSetCategory = Category[FinSetObject, FinSetMorphism]
FinSetInitialObject = InitialObject[FinSetObject, FinSetMorphism]
FinSetTerminalObject = TerminalObject[FinSetObject, FinSetMorphism]
FinSetCoProductCoCone = CoProductCoCone[FinSetObject, FinSetMorphism]
FinSetProductCone = ProductCone[FinSetObject, FinSetMorphism]
FinSetCoEqualizerCoCone = CoEqualizerCoCone[FinSetObject, FinSetMorphism]
FinSetEqualizerCone = EqualizerCone[FinSetObject, FinSetMorphism]
FinSetPushoutCoCone = PushoutCoCone[FinSetObject, FinSetMorphism]
FinSetPullbackCone = PullbackCone[FinSetObject, FinSetMorphism]

finset_category = FinSetCategory(finset_source, finset_target, finset_identity, finset_composition)

finset_terminal_obj_value = None

finset_initial_obj_ = FinSetObject(())


def finset_initial_obj_univ(a: FinSetObject) -> FinSetMorphism:
    return FinSetMorphism(finset_initial_obj_, a, nil_fn)


finset_initial_obj = FinSetInitialObject(finset_initial_obj_, finset_initial_obj_univ)


finset_terminal_obj_ = FinSetObject((finset_terminal_obj_value,))


def finset_terminal_obj_univ_proj(a: _FST) -> _FST:
    return finset_terminal_obj_value


def finset_terminal_obj_univ(a: FinSetObject) -> FinSetMorphism:
    return FinSetMorphism(a, finset_terminal_obj_, finset_terminal_obj_univ_proj)


finset_terminal_obj = FinSetTerminalObject(finset_terminal_obj_, finset_terminal_obj_univ)


def finset_coproduct(a: FinSetObject, b: FinSetObject) -> FinSetCoProductCoCone:
    def label_0(x: _FST) -> _FST:
        return x, 0

    def label_1(x: _FST) -> _FST:
        return x, 1

    disjoint_union: FinSetObject = FinSetObject(list(map(label_0, a)) + list(map(label_1, b)))
    label_a = FinSetMorphism(a, disjoint_union, label_0)
    label_b = FinSetMorphism(b, disjoint_union, label_1)

    def finset_coproduct_univ(p: FinSetMorphism, q: FinSetMorphism) -> FinSetMorphism:
        assert p.cod == q.cod
        assert p.dom == a and q.dom == b

        univ_dict: Dict[_FST, _FST] = {}
        for x in a:
            univ_dict[label_a(x)] = p(x)
        for x in b:
            univ_dict[label_b(x)] = q(x)

        def univ_map(x: _FST) -> _FST:
            assert x in disjoint_union
            return univ_dict[x]

        return FinSetMorphism(disjoint_union, p.cod, univ_map)

    return FinSetCoProductCoCone(disjoint_union, label_a, label_b, finset_coproduct_univ)


def finset_product(a: FinSetObject, b: FinSetObject) -> FinSetProductCone:
    cartesian_product: FinSetObject = FinSetObject(product(a, b))

    def proj_a_(x: _FST) -> _FST:
        return x[0]  # type: ignore

    def proj_b_(x: _FST) -> _FST:
        return x[1]  # type: ignore

    proj_a = FinSetMorphism(cartesian_product, a, proj_a_)
    proj_b = FinSetMorphism(cartesian_product, b, proj_b_)

    def finset_product_univ(p: FinSetMorphism, q: FinSetMorphism) -> FinSetMorphism:
        assert p.dom == q.dom
        assert p.cod == a and q.cod == b

        def univ_map(x: _FST) -> _FST:
            return (p(x), q(x))

        return FinSetMorphism(p.dom, cartesian_product, univ_map)

    return FinSetProductCone(cartesian_product, proj_a, proj_b, finset_product_univ)


def partition(elements: Iterable[_FST], equivalences: List[Tuple[_FST, _FST]]) -> Dict[_FST, _FST]:
    # Simplified version of https://networkx.org/documentation/stable/_modules/networkx/utils/union_find.html.
    parents = {}
    weights = {}
    for x in elements:
        parents[x] = x
        weights[x] = 1

    def find(x: _FST) -> _FST:
        path = []
        root = parents[x]
        while root != x:
            path.append(x)
            x = root
            root = parents[x]

        for ancestor in path:
            parents[ancestor] = root
        return root

    for x, y in equivalences:
        rx, ry = find(x), find(y)
        if rx == ry:
            continue

        wx, wy = weights[rx], weights[ry]
        if wy > wx:
            (y, ry, wy), (x, rx, wx) = (x, rx, wx), (y, ry, wy)

        parents[ry] = rx
        weights[rx] += wy

    for x in parents:
        find(x)

    parent_to_equivalence_class = defaultdict(list)
    for x, parent in parents.items():
        parent_to_equivalence_class[parent].append(x)

    element_to_equivalence_class: Dict[_FST, _FST] = {}
    for x, parent in parents.items():
        element_to_equivalence_class[x] = frozenset(parent_to_equivalence_class[parent])

    return element_to_equivalence_class


def finset_coequalizer(f: FinSetMorphism, g: FinSetMorphism) -> FinSetCoEqualizerCoCone:
    assert f.dom == g.dom and f.cod == g.cod

    quotient_map_dict = partition(f.cod, [(f(a), g(a)) for a in f.dom])

    def quotient_map(a: _FST) -> _FST:
        return quotient_map_dict[a]

    partitions_obj = FinSetObject(quotient_map_dict.values())

    def finset_coequalizer_univ(q: FinSetMorphism) -> FinSetMorphism:
        assert q.dom == f.cod
        assert all(finset_composition(q, f)(x) == finset_composition(q, g)(x) for x in f.dom)

        def univ_map(x: _FST) -> _FST:
            assert x in partitions_obj
            return q(next(iter(x)))  # type: ignore

        return FinSetMorphism(partitions_obj, q.cod, univ_map)

    return FinSetCoEqualizerCoCone(
        partitions_obj, FinSetMorphism(f.cod, partitions_obj, quotient_map), finset_coequalizer_univ
    )


def finset_inclusion(a: FinSetObject, b: FinSetObject) -> FinSetMorphism:
    def finset_id_(x: _FST) -> _FST:
        return x

    return FinSetMorphism(a, b, finset_id_)


def finset_equalizer(f: FinSetMorphism, g: FinSetMorphism) -> FinSetEqualizerCone:
    a = f.dom
    subset = FinSetObject(x for x in a if f(x) == g(x))

    def finset_equalizer_univ(p: FinSetMorphism) -> FinSetMorphism:
        assert p.cod == a, (p.cod, a)
        assert all(finset_composition(f, p)(x) == finset_composition(g, p)(x) for x in p.dom)

        def univ_map(x: _FST) -> _FST:
            return p(x)

        return FinSetMorphism(p.dom, subset, univ_map)

    return FinSetEqualizerCone(subset, finset_inclusion(subset, a), finset_equalizer_univ)


FinSetCoComplete = CoCompleteCategory[FinSetObject, FinSetMorphism]
FinSetComplete = CompleteCategory[FinSetObject, FinSetMorphism]

finset_cocomplete = FinSetCoComplete(finset_category, finset_coproduct, finset_coequalizer)
finset_complete = FinSetComplete(finset_category, finset_product, finset_equalizer)

FinSetPushout = Pushout[FinSetMorphism, FinSetObject]
FinSetPullback = Pullback[FinSetMorphism, FinSetObject]


def finset_pushout(f: FinSetMorphism, g: FinSetMorphism) -> FinSetPushoutCoCone:
    assert f.dom == g.dom
    cp = finset_coproduct(f.cod, g.cod)
    ce = finset_coequalizer(finset_composition(cp.proj_a, f), finset_composition(cp.proj_b, g))

    def finset_pushout_univ(u: FinSetMorphism, v: FinSetMorphism) -> FinSetMorphism:
        assert u.cod == v.cod
        assert u.dom == f.cod and v.dom == g.cod
        assert all(finset_composition(u, f)(x) == finset_composition(v, g)(x) for x in f.dom)
        return ce.univ(cp.univ(u, v))

    return FinSetPushoutCoCone(
        ce.apex,
        finset_composition(ce.proj, cp.proj_a),
        finset_composition(ce.proj, cp.proj_b),
        finset_pushout_univ,
    )


def finset_pullback(f: FinSetMorphism, g: FinSetMorphism) -> FinSetPullbackCone:
    assert f.cod == g.cod
    p = finset_product(f.dom, g.dom)
    e = finset_equalizer(finset_composition(f, p.proj_a), finset_composition(g, p.proj_b))

    def finset_pullback_univ(u: FinSetMorphism, v: FinSetMorphism) -> FinSetMorphism:
        assert u.dom == v.dom
        assert u.cod == f.dom and v.cod == g.dom
        assert all(finset_composition(f, u)(x) == finset_composition(g, v)(x) for x in u.dom)
        return e.univ(p.univ(u, v))

    return FinSetPullbackCone(
        e.apex, finset_composition(p.proj_a, e.proj), finset_composition(p.proj_b, e.proj), finset_pullback_univ
    )


def finset_pushout_complement(
    f_or_g: FinSetMorphism, proj_b_or_c: FinSetMorphism, pushout_apex: FinSetObject
) -> Tuple[FinSetObject, FinSetMorphism, FinSetMorphism]:
    assert f_or_g.cod == proj_b_or_c.dom
    assert proj_b_or_c.cod == pushout_apex
    assert is_injective(f_or_g)

    apex_less_b_or_c = pushout_apex - set(map(proj_b_or_c, f_or_g.cod))
    proj_b_or_c_f_or_g = finset_composition(proj_b_or_c, f_or_g)
    mapped_f_or_g_dom = map(proj_b_or_c_f_or_g, f_or_g.dom)
    complement = FinSetObject(apex_less_b_or_c.union(mapped_f_or_g_dom))

    proj_c_or_b = FinSetMorphism(complement, pushout_apex, lambda a: a)
    g_or_f = FinSetMorphism(f_or_g.dom, complement, lambda a: proj_b_or_c_f_or_g(a))

    return complement, g_or_f, proj_c_or_b
