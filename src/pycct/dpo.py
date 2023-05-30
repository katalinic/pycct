from dataclasses import dataclass

from .fingraph import FinGraphMorphism, FinGraphObject, fingraph_pushout, fingraph_pushout_complement


@dataclass(eq=False, frozen=True, repr=False)
class DoublePushoutRule:
    precondition_map: FinGraphMorphism
    postcondition_map: FinGraphMorphism

    def __post_init__(self) -> None:
        assert self.precondition_map.dom == self.postcondition_map.dom


def double_pushout(rule: DoublePushoutRule, before: FinGraphObject, match: FinGraphMorphism) -> FinGraphObject:
    _, condition_to_context, _ = fingraph_pushout_complement(rule.precondition_map, match, before)
    after_pushout = fingraph_pushout(rule.postcondition_map, condition_to_context)
    return after_pushout.apex
