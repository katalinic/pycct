from .lsa import peano_tree_to_str, str_to_peano_tree
from .lsa_increment_last import lsa_increment_last


def test_str_to_peano_tree():
    tree = str_to_peano_tree("abc")
    assert tree.nodes == frozenset({"C_0", "C_1", "C_2", "S_1_1", "S_2_1", "S_2_2"})
    assert tree.edges == frozenset({"C_0_1", "C_1_2", "S_1_0_1", "S_2_0_1", "S_2_1_2"})
    assert all(
        tree.source(edge) == expected
        for edge, expected in [
            ("C_0_1", "C_0"),
            ("C_1_2", "C_1"),
            ("S_1_0_1", "C_1"),
            ("S_2_0_1", "C_2"),
            ("S_2_1_2", "S_2_1"),
        ]
    )
    assert all(
        tree.target(edge) == expected
        for edge, expected in [
            ("C_0_1", "C_1"),
            ("C_1_2", "C_2"),
            ("S_1_0_1", "S_1_1"),
            ("S_2_0_1", "S_2_1"),
            ("S_2_1_2", "S_2_2"),
        ]
    )


def test_peano_tree_to_str():
    assert peano_tree_to_str(str_to_peano_tree("abc")) == "abc"
    assert peano_tree_to_str(str_to_peano_tree("ijl")) == "ijl"


def test_lsa():
    assert lsa_increment_last("abc", "abd", "ijk") == "ijl"
    assert lsa_increment_last("abc", "abd", "ddd") == "dde"
    assert lsa_increment_last("aabbcc", "aabbcd", "mmjjkk") == "mmjjkl"
