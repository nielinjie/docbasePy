from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar
from attr import dataclass

T = TypeVar("T")


class NeedPrepare(Generic[T], ABC):
    @abstractmethod
    def fold(self, doneFun: Callable[[T], Any], notReadyFun: Callable[[], Any]):
        pass


@dataclass
class Preparing(NeedPrepare[T]):

    def fold(self, doneFun: Callable[[T], Any], notReadyFun: Callable[[], Any]):
        return notReadyFun()


@dataclass
class NotStarted(NeedPrepare[T]):

    def fold(self, doneFun: Callable[[T], Any], notReadyFun: Callable[[], Any]):
        return notReadyFun()


@dataclass
class Done(NeedPrepare[T]):
    result: T

    def fold(self, doneFun: Callable[[T], Any], notReadyFun: Callable[[], Any]):
        return doneFun(self.result)
