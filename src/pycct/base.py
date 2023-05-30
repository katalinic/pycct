from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


class Object:
    pass


class Morphism:
    dom: Object
    cod: Object


_OT = TypeVar("_OT", bound=Object)
_MT = TypeVar("_MT", bound=Morphism)


@dataclass(frozen=True, repr=False)
class Category(Generic[_OT, _MT]):
    source: Callable[[_MT], _OT]
    target: Callable[[_MT], _OT]
    identity: Callable[[_OT], _MT]
    composition: Callable[[_MT, _MT], _MT]


@dataclass(frozen=True, repr=False)
class InitialObject(Generic[_OT, _MT]):
    value: _OT
    univ: Callable[[_OT], _MT]


@dataclass(frozen=True, repr=False)
class TerminalObject(InitialObject[_OT, _MT]):
    pass


@dataclass(frozen=True, repr=False)
class CoProductCoCone(Generic[_OT, _MT]):
    apex: _OT
    proj_a: _MT
    proj_b: _MT
    univ: Callable[[_MT, _MT], _MT]


@dataclass(frozen=True, repr=False)
class ProductCone(CoProductCoCone[_OT, _MT]):
    pass


@dataclass(frozen=True, repr=False)
class CoEqualizerCoCone(Generic[_OT, _MT]):
    apex: _OT
    proj: _MT
    univ: Callable[[_MT], _MT]


@dataclass(frozen=True, repr=False)
class EqualizerCone(CoEqualizerCoCone[_OT, _MT]):
    pass


@dataclass(frozen=True, repr=False)
class PushoutCoCone(Generic[_OT, _MT]):
    apex: _OT
    proj_b: _MT
    proj_c: _MT
    univ: Callable[[_MT, _MT], _MT]


@dataclass(frozen=True, repr=False)
class PullbackCone(PushoutCoCone[_OT, _MT]):
    pass


CoProduct = Callable[[_OT, _OT], CoProductCoCone[_OT, _MT]]
Product = Callable[[_OT, _OT], ProductCone[_OT, _MT]]
CoEqualizer = Callable[[_MT, _MT], CoEqualizerCoCone[_OT, _MT]]
Equalizer = Callable[[_MT, _MT], EqualizerCone[_OT, _MT]]
Pushout = Callable[[_MT, _MT], PushoutCoCone[_OT, _MT]]
Pullback = Callable[[_MT, _MT], PullbackCone[_OT, _MT]]


@dataclass(frozen=True, repr=False)
class CoCompleteCategory(Generic[_OT, _MT]):
    cat: Category[_OT, _MT]
    coprod: CoProduct[_OT, _MT]
    coeq: CoEqualizer[_MT, _OT]


@dataclass(frozen=True, repr=False)
class CompleteCategory(Generic[_OT, _MT]):
    cat: Category[_OT, _MT]
    prod: Product[_OT, _MT]
    eq: Equalizer[_MT, _OT]
