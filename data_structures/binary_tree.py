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

    """反序列化"""
    def deserialize(
        self,
        series: list[Optional[T]],
        order: Literal["pre", "post", "level"],
        disable_recursion: bool = False
    ):
        if order == "pre":
            if disable_recursion:
                self.root = self.__deserialize_preorder_no_recur(series)
            else:
                self.root = self.__deserialize_preorder(series)
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
            if disable_recursion:
                yield from self.__preorder_traverse_no_recur(self.root)
            else:
                yield from self.__preorder_traverse(self.root)
        else:
            raise NotImplementedError("not implemented")

    """可视化"""
    def visualize(self) -> None:
        if (self.root is None):
            return
        self.__visualize_node(self.root)

    """前序遍历反序列化"""
    @classmethod
    def __deserialize_preorder(cls, series: list[Optional[T]]) -> Optional[BinaryTreeNode[T]]:
        series_que = Queue(series)
        def deserialize() -> Optional[BinaryTreeNode[T]]:
            if series_que.is_empty():
                return None
            val = series_que.pop()
            if val is None:
                return None
            root: BinaryTreeNode[T] = BinaryTreeNode(val)  # type:ignore
            root.left = deserialize()
            root.right = deserialize()
            return root
        return deserialize()

    """前序遍历反序列化(非递归)"""
    @classmethod
    def __deserialize_preorder_no_recur(cls, series: list[Optional[T]]) -> Optional[BinaryTreeNode[T]]:
        series_que = Queue(series)
        root_val = series_que.pop()
        if root_val is None:
            return None
        node_stk = Stack[BinaryTreeNode[T]]()
        root = BinaryTreeNode(root_val)
        node_stk.push(root)
        while not series_que.is_empty():
            r"""循环逻辑
                                       ...
                                        |
                                        O
                                      /
                                     O
                                   /   \
                                  O     O  <- (2) 找到下一轮循环起点
                                 / \   /
            (1)找到左子树栈尽头 -> X  X  ...
            """
            while series_que.front() is not None:  # (1)
                new_node = BinaryTreeNode[T](series_que.pop())  # type:ignore
                node_stk.top().left = new_node
                node_stk.push(new_node)
            assert series_que.pop() is None, ValueError("invalid series")  # (2)
            while not series_que.is_empty() and series_que.front() is None:
                series_que.pop()
                node_stk.pop()
            if not series_que.is_empty():
                new_node = BinaryTreeNode[T](series_que.pop())  # type:ignore
                node_stk.pop().right = new_node
                node_stk.push(new_node)
        return root

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

    """前序遍历（非递归）"""
    @classmethod
    def __preorder_traverse_no_recur(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        stk = Stack[Optional[BinaryTreeNode[T]]]()
        stk.push(root)
        while not stk.is_empty():
            node = stk.pop()
            yield node
            if node is not None:
                stk.push(node.right)
                stk.push(node.left)

    """中序遍历"""
    @classmethod
    def __inorder_traverse(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        if root is None:
            yield root
        else:
            yield from cls.__preorder_traverse(root.left)
            yield root
            yield from cls.__preorder_traverse(root.right)

    """后序遍历"""
    @classmethod
    def __postorder_traverse(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        if root is None:
            yield root
        else:
            yield from cls.__preorder_traverse(root.left)
            yield from cls.__preorder_traverse(root.right)
            yield root

    @classmethod
    def __visualize_node(cls, node: BinaryTreeNode[T], prefix: str = "", is_left: bool = True):
        if node.right:
            cls.__visualize_node(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        if node.left:
            cls.__visualize_node(node.left, prefix + ("    " if is_left else "│   "), True)

if __name__ == "__main__":
    print("[preorder]")
    preorder: list[Optional[int]] = [1, 2, 3, 4, None, None, 5, 6, None, None, None, 7, None, None, 8, None, 9, None, None]
    tree = BinaryTree[int]()
    print("\n  * with recursion")
    tree.deserialize(preorder, "pre")
    tree.visualize()
    print(tree.serialize("pre"))
    print("\n  * without recursion")
    tree.deserialize(preorder, "pre", True)
    tree.visualize()
    print(tree.serialize("pre", True))