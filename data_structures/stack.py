from typing import TypeVar, Generic, Optional


T = TypeVar("T")


class Stack(Generic[T]):

    def __init__(self, values: Optional[list[T]] = None):
        self.__list: list[T] = []
        if values is not None:
            for v in values:
                self.push(v)

    def push(self, element: T) -> None:
        self.__list.append(element)

    def pop(self) -> None:
        try:
            self.__list.pop()
        except IndexError:
            raise BufferError("stack is empty")

    def top(self) -> T:
        if len(self.__list) == 0:
            raise BufferError("stack is empty")
        else:
            return self.__list[-1]

    def size(self) -> int:
        return len(self.__list)

    def is_empty(self) -> bool:
        return len(self.__list) == 0
