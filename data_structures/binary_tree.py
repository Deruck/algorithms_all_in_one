from typing import Optional, TypeVar, Generic, Generator, Literal
from dataclasses import dataclass

from stack import Stack
from queue_ import Queue

NULL_REPR = "null"
SERIALIZE_SPLIT = ", "

T = TypeVar("T")
@dataclass
class BinaryTreeNode(Generic[T]):
    val: T
    left: Optional["BinaryTreeNode[T]"] = None
    right: Optional["BinaryTreeNode[T]"] = None

    def __str__(self) -> str:
        return str(self.val)


class BinaryTree(Generic[T]):

    def __init__(self):
        self.root: Optional[BinaryTreeNode[T]] = None

    """带 null 信息的反序列化"""
    def construct_from_full(
        self,
        series: list[Optional[T]],
        order: Literal["pre", "post", "level"],
        disable_recursion: bool = False
    ):
        if order == "pre" and not disable_recursion:
            self.root = self.__construct_from_full_preorder(series)
        else:
            raise NotImplementedError("not implemented") 

    """序列化"""
    def serialize(
        self,
        order: Literal["pre", "post", "in", "level"],
        disable_recursion: bool = False
    ):
        traverse_result = [str(node) for node in self.traverse(order, disable_recursion)]
        return SERIALIZE_SPLIT.join(traverse_result)

    """遍历"""
    def traverse(
        self,
        order: Literal["pre", "post", "in", "level"],
        disable_recursion: bool = False
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        if order == "pre":
            yield from self.__preorder_traverse(self.root)
        else:
            yield None

    """可视化"""
    def visualize(self) -> None:
        if (self.root is None):
            return
        self.__visualize_node(self.root)

    """前序遍历反序列化"""
    @classmethod
    def __construct_from_full_preorder(cls, series: list[Optional[T]]) -> Optional[BinaryTreeNode[T]]:
        series_que = Queue(series)
        def construct() -> Optional[BinaryTreeNode[T]]:
            if series_que.is_empty():
                return None
            if series_que.front() is None:
                series_que.pop()
                return None
            root: BinaryTreeNode[T] = BinaryTreeNode(series_que.front())  # type:ignore
            series_que.pop()
            root.left = construct()
            root.right = construct()
            return root
        return construct()

    """前序遍历"""
    @classmethod
    def __preorder_traverse(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        if root is None:
            yield root
        else:
            yield root
            yield from cls.__preorder_traverse(root.left)
            yield from cls.__preorder_traverse(root.right)

    @classmethod
    def __visualize_node(cls, node: BinaryTreeNode[T], prefix: str = "", is_left: bool = True):
        if node.right:
            cls.__visualize_node(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        if node.left:
            cls.__visualize_node(node.left, prefix + ("    " if is_left else "│   "), True)


if __name__ == "__main__":
    preorder: list[Optional[int]] = [1, 2, 3, 4, None, None, 5, 6, None, None, None, 7, None, None, 8, None, 9, None, None]
    tree = BinaryTree[int]()
    tree.construct_from_full(preorder, "pre")
    tree.visualize()
    print(tree.serialize("pre"))