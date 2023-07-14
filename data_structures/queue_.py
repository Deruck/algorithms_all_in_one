from collections import deque
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class Queue(Generic[T]):

    def __init__(self, values: Optional[list[T]] = None):
        self.__deq = deque[T]()
        if values is not None:
            for v in values:
                self.push(v)

    def push(self, val: T) -> None:
        self.__deq.append(val)

    def front(self) -> T:
        if (len(self.__deq) == 0):
            raise BufferError("queue is empty")
        return self.__deq[0]

    def pop(self) -> None:
        if (len(self.__deq) == 0):
            raise BufferError("queue is empty")
        self.__deq.popleft()

    def size(self) -> int:
        return len(self.__deq)

    def is_empty(self) -> bool:
        return len(self.__deq) == 0
