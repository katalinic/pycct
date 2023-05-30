from pycct import (
    FinSetMorphism,
    FinSetObject,
    finset_coequalizer,
    finset_composition,
    finset_coproduct,
    finset_equalizer,
    finset_product,
    finset_pullback,
    finset_pushout,
    finset_pushout_complement,
)


def test_coproduct():
    a = FinSetObject(["A", "B", "C"])
    b = FinSetObject(["C", "S", "T"])
    coproduct = finset_coproduct(a, b)
    assert coproduct.apex == frozenset([("A", 0), ("B", 0), ("C", 0), ("C", 1), ("S", 1), ("T", 1)])
    assert frozenset(map(coproduct.proj_a, a)).union(frozenset(map(coproduct.proj_b, b))) == coproduct.apex

    candidate = FinSetObject(["A", "B", "C", "S", "T"])
    p = FinSetMorphism(a, candidate, lambda x: x)
    q = FinSetMorphism(b, candidate, lambda x: x)
    univ = coproduct.univ(p, q)
    assert univ.dom == coproduct.apex
    assert univ.cod == candidate
    assert frozenset(map(univ, coproduct.apex)) == candidate
    assert all(finset_composition(univ, coproduct.proj_a)(x) == p(x) for x in a)
    assert all(finset_composition(univ, coproduct.proj_b)(x) == q(x) for x in b)


def test_product():
    a = FinSetObject(["A", "B", "C"])
    b = FinSetObject(["S", "T"])
    product = finset_product(a, b)
    assert product.apex == frozenset([("A", "S"), ("A", "T"), ("B", "S"), ("B", "T"), ("C", "S"), ("C", "T")])
    assert frozenset(map(product.proj_a, product.apex)) == a
    assert frozenset(map(product.proj_b, product.apex)) == b

    candidate = FinSetObject(["A", "B", "C", "S", "T"])
    p = FinSetMorphism(candidate, a, lambda x: "C" if x in ("S", "T") else x)
    q = FinSetMorphism(candidate, b, lambda x: "S" if x in ("A", "B", "C") else x)
    univ = product.univ(p, q)
    assert univ.dom == candidate
    assert univ.cod == product.apex
    assert frozenset(map(univ, candidate)).issubset(product.apex)
    assert all(finset_composition(product.proj_a, univ)(x) == p(x) for x in candidate)
    assert all(finset_composition(product.proj_b, univ)(x) == q(x) for x in candidate)


def test_coequalizer():
    a = FinSetObject(["A", "B", "C", "D"])
    b = FinSetObject(["C", "D", "E", "F", "G"])

    f_dict = {"A": "C", "B": "C", "C": "D", "D": "E"}
    g_dict = {"A": "D", "B": "D", "C": "F", "D": "G"}

    def f_(e):
        return f_dict[e]

    def g_(e):
        return g_dict[e]

    f = FinSetMorphism(a, b, f_)
    g = FinSetMorphism(a, b, g_)

    coequalizer = finset_coequalizer(f, g)
    assert coequalizer.apex == frozenset(
        [
            frozenset({"C", "D", "F"}),
            frozenset({"E", "G"}),
        ]
    )
    assert frozenset(map(coequalizer.proj, b)).issubset(coequalizer.apex)

    candidate = FinSetObject([frozenset({"C"}), frozenset({"E"})])
    q = FinSetMorphism(b, candidate, lambda x: frozenset({"E"}) if x in ("E", "G") else frozenset({"C"}))
    univ = coequalizer.univ(q)
    assert univ.dom == coequalizer.apex
    assert univ.cod == candidate
    assert frozenset(map(univ, coequalizer.apex)) == candidate
    assert all(finset_composition(univ, coequalizer.proj)(x) == q(x) for x in b)


def test_equalizer():
    a = FinSetObject(["A", "B", "C", "D"])
    b = FinSetObject(["C", "D", "E", "F", "G"])

    f_dict = {"A": "C", "B": "D", "C": "D", "D": "G"}
    g_dict = {"A": "D", "B": "D", "C": "F", "D": "G"}

    def f_(e):
        return f_dict[e]

    def g_(e):
        return g_dict[e]

    f = FinSetMorphism(a, b, f_)
    g = FinSetMorphism(a, b, g_)

    equalizer = finset_equalizer(f, g)
    assert equalizer.apex == frozenset(["B", "D"])
    assert frozenset(map(equalizer.proj, equalizer.apex)) == equalizer.apex
    assert frozenset(map(equalizer.proj, equalizer.apex)).issubset(a)

    candidate = FinSetObject(["B"])
    p = FinSetMorphism(candidate, a, lambda x: x)
    univ = equalizer.univ(p)
    assert univ.dom == candidate
    assert univ.cod == equalizer.apex
    assert frozenset(map(univ, candidate)).issubset(equalizer.apex)
    assert all(finset_composition(equalizer.proj, univ)(x) == p(x) for x in candidate)


def test_pushout():
    a = FinSetObject(["A", "B", "C", "D"])
    b = FinSetObject(["C", "D", "E", "F", "G"])
    c = FinSetObject(["B", "E", "F", "G"])

    f_dict = {"A": "C", "B": "C", "C": "D", "D": "E"}
    g_dict = {"A": "B", "B": "E", "C": "B", "D": "F"}

    def f_(e):
        return f_dict[e]

    def g_(e):
        return g_dict[e]

    f = FinSetMorphism(a, b, f_)
    g = FinSetMorphism(a, c, g_)

    pushout = finset_pushout(f, g)
    assert pushout.apex == frozenset(
        [
            frozenset({("G", 0)}),
            frozenset({("F", 0)}),
            frozenset({("G", 1)}),
            frozenset({("F", 1), ("E", 0)}),
            frozenset({("C", 0), ("E", 1), ("B", 1), ("D", 0)}),
        ]
    )

    assert frozenset(map(pushout.proj_b, b)).union(frozenset(map(pushout.proj_c, c))) == pushout.apex
    assert all(finset_composition(pushout.proj_b, f)(x) == finset_composition(pushout.proj_c, g)(x) for x in a)

    candidate = FinSetObject(
        [
            frozenset({("G", 0)}),
            frozenset({("F", 0)}),
            frozenset({("G", 1)}),
            frozenset({("E", 0)}),
            frozenset({("D", 0)}),
        ]
    )
    candidate_b_dict = {
        "C": frozenset({("D", 0)}),
        "D": frozenset({("D", 0)}),
        "E": frozenset({("E", 0)}),
        "F": frozenset({("F", 0)}),
        "G": frozenset({("G", 0)}),
    }
    candidate_c_dict = {
        "B": frozenset({("D", 0)}),
        "E": frozenset({("D", 0)}),
        "F": frozenset({("E", 0)}),
        "G": frozenset({("G", 1)}),
    }
    p = FinSetMorphism(b, candidate, lambda x: candidate_b_dict[x])
    q = FinSetMorphism(c, candidate, lambda x: candidate_c_dict[x])
    univ = pushout.univ(p, q)
    assert univ.dom == pushout.apex
    assert univ.cod == candidate
    assert frozenset(map(univ, pushout.apex)) == candidate
    assert all(finset_composition(univ, pushout.proj_b)(x) == p(x) for x in b)
    assert all(finset_composition(univ, pushout.proj_c)(x) == q(x) for x in c)


def test_pullback():
    a = FinSetObject(["A", "B", "C", "D"])
    b = FinSetObject(["C", "D", "E", "F", "G"])
    c = FinSetObject(["B", "E", "F", "G"])

    f_dict = {"C": "A", "D": "B", "E": "B", "F": "D", "G": "D"}
    g_dict = {"B": "A", "E": "B", "F": "C", "G": "D"}

    def f_(e):
        return f_dict[e]

    def g_(e):
        return g_dict[e]

    f = FinSetMorphism(b, a, f_)
    g = FinSetMorphism(c, a, g_)

    pullback = finset_pullback(f, g)
    assert pullback.apex == frozenset(
        [
            ("C", "B"),
            ("D", "E"),
            ("E", "E"),
            ("F", "G"),
            ("G", "G"),
        ]
    )
    assert frozenset(map(pullback.proj_b, pullback.apex)).issubset(b)
    assert frozenset(map(pullback.proj_c, pullback.apex)).issubset(c)
    assert all(
        finset_composition(f, pullback.proj_b)(x) == finset_composition(g, pullback.proj_c)(x) for x in pullback.apex
    )

    candidate = FinSetObject([("C", "B"), ("F", "G"), ("G", "G")])
    p = FinSetMorphism(candidate, b, lambda x: x[0])
    q = FinSetMorphism(candidate, c, lambda x: x[1])
    univ = pullback.univ(p, q)
    assert univ.dom == candidate
    assert univ.cod == pullback.apex
    assert frozenset(map(univ, candidate)).issubset(pullback.apex)
    assert frozenset(map(univ, candidate)) == candidate
    assert all(finset_composition(pullback.proj_b, univ)(x) == p(x) for x in candidate)
    assert all(finset_composition(pullback.proj_c, univ)(x) == q(x) for x in candidate)


def test_pushout_complement():
    a = FinSetObject(["A", "B", "C"])
    b = FinSetObject(["C", "D", "E", "F", "G"])
    c = FinSetObject(["A", "B", "F", "G"])

    f_dict = {"A": "C", "B": "E", "C": "F"}
    g_dict = {"A": "A", "B": "B", "C": "F"}

    def f_(e):
        return f_dict[e]

    def g_(e):
        return g_dict[e]

    f = FinSetMorphism(a, b, f_)
    g = FinSetMorphism(a, c, g_)

    pushout = finset_pushout(f, g)
    pushout_complement, f_complement, proj_b_complement = finset_pushout_complement(g, pushout.proj_c, pushout.apex)

    assert pushout_complement == frozenset(
        [
            frozenset({("C", 0), ("A", 1)}),
            frozenset({("D", 0)}),
            frozenset({("E", 0), ("B", 1)}),
            frozenset({("F", 0), ("F", 1)}),
            frozenset({("G", 0)}),
        ]
    )
    assert frozenset(map(f_complement, a)).issubset(pushout_complement)
    assert frozenset(map(proj_b_complement, pushout_complement)).issubset(pushout.apex)
    assert all(
        finset_composition(proj_b_complement, f_complement)(x) == finset_composition(pushout.proj_c, g)(x) for x in a
    )
