from typing import Optional, TypeVar, Generic, Generator, Literal, Type
from dataclasses import dataclass

from stack import Stack
from queue_ import Queue

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
        series: str,
        order: Literal["pre", "post", "level"],
        disable_recursion: bool = False, 
        split: str = ", ",
        null_repr: str = "null"
    ):
        str_list = series.split(split)
        val_list = [self.__get_type()(s) if s != null_repr else None
                    for s in str_list]
        if order == "pre":
            if disable_recursion:
                self.root = self.__deserialize_preorder_no_recur(val_list)
            else:
                self.root = self.__deserialize_preorder(val_list)
        else:
            raise NotImplementedError("not implemented") 

    """序列化"""
    def serialize(
        self,
        order: Literal["pre", "post", "in", "level"],
        disable_recursion: bool = False,
        split: str = ", ",
        null_repr: str = "null"
    ):
        traverse_result = [str(node) if node is not None else null_repr 
                           for node in self.traverse(order, disable_recursion)]
        return split.join(traverse_result)

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
        elif order == "in" and not disable_recursion:
            yield from self.__inorder_traverse(self.root)
        elif order == "post" and not disable_recursion:
            yield from self.__postorder_traverse(self.root)
        elif order == "level":
            yield from self.__levelorder_traverse(self.root)
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
                                                      /
                                                     O
                                                    /
                                                   O
                                                 /   \
                                                O     O  <- (2) 找到下一轮循环起点(连续null后的第一个非null节点)
                                               / \   /
            (1)找到左子树栈尽头(第一个null节点) -> X  X  ...  <- (3) 下一轮循环
            """
            while series_que.front() is not None:  # (1)
                new_node = BinaryTreeNode[T](series_que.pop())  # type:ignore
                node_stk.top().left = new_node
                node_stk.push(new_node)
            assert series_que.pop() is None, ValueError("invalid series")
            while not series_que.is_empty() and series_que.front() is None:  # (2)
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
            yield from cls.__inorder_traverse(root.left)
            yield root
            yield from cls.__inorder_traverse(root.right)

    """后序遍历"""
    @classmethod
    def __postorder_traverse(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        if root is None:
            yield root
        else:
            yield from cls.__postorder_traverse(root.left)
            yield from cls.__postorder_traverse(root.right)
            yield root

    """层序遍历"""
    @classmethod
    def __levelorder_traverse(
        cls, 
        root: Optional[BinaryTreeNode[T]]
    ) -> Generator[Optional[BinaryTreeNode[T]], None, None]:
        que = Queue[Optional[BinaryTreeNode]]()
        que.push(root)
        while not que.is_empty():
            node = que.pop()
            yield node
            if node is not None:
                que.push(node.left)
                que.push(node.right)

    @classmethod
    def __visualize_node(cls, node: BinaryTreeNode[T], prefix: str = "", is_left: bool = True):
        if node.right:
            cls.__visualize_node(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        if node.left:
            cls.__visualize_node(node.left, prefix + ("    " if is_left else "│   "), True)

    def __get_type(self) -> Type[T]:
        return self.__orig_class__.__args__[0]  # type: ignore




if __name__ == "__main__":
    """
    │       ┌── 9
    │       │   └── 10
    │   ┌── 8
    └── 1
        │   ┌── 7
        └── 2
            │   ┌── 5
            │   │   └── 6
            └── 3
                └── 4
    """
    print("\nTree\n")
    tree = BinaryTree[int]()
    preorder = "1, 2, 3, 4, null, null, 5, 6, null, null, null, 7, null, null, 8, null, 9, 10, null, null, null"
    tree.deserialize(preorder, "pre")
    tree.visualize()

    print("\n* preorder with recursion")
    print(f"  * serialize: {tree.serialize('pre')}")
    print("  * deserialize: ")
    tree.deserialize(preorder, "pre")
    tree.visualize()
    print("\n* preorder without recursion")
    print(f"  * serialize: {tree.serialize('pre', True)}")
    print("  * deserialize: ")
    tree.deserialize(preorder, "pre", True)
    tree.visualize()

    print("\n* inorder with recursion")
    print(f"  * serialize: {tree.serialize('in')}")

    print("\n* postorder with recursion")
    print(f"  * serialize: {tree.serialize('post')}")

    print("\n* levelorder")
    print(f"  * serialize: {tree.serialize('level')}")