import os
import re
import pytest

from enum import Enum, auto


class NodeType(Enum):
    FILE = auto()
    DIR = auto()


class FileNode:
    def __init__(self, name: str, size: int = 0, parent: "FileNode" = None):
        self._children = []
        self.name = name
        self.size = size
        self.parent = parent

        if parent:
            parent.add_child(self)

    @property
    def node_type(self):
        return NodeType.DIR if self.children else NodeType.FILE

    @property
    def children(self):
        return self._children

    def add_child(self, child: "FileNode"):
        if child.name in {ch.name for ch in self._children}:
            raise ValueError(
                f"File named {child.name} already exists in dir {self.name}"
            )
        self._children.append(child)
        child.parent = self

        dir_node = self
        while dir_node:
            dir_node.size += child.size
            dir_node = dir_node.parent

    def generate_dirs(self):
        if self.node_type != NodeType.DIR:
            return

        yield self
        for file_node in self._children:
            if file_node.node_type == NodeType.DIR:
                yield from file_node.generate_dirs()

    def __equals__(self, other):
        return (
            self.name == other.name
            and [ch.name for ch in self._children]
            == [other_ch.name for other_ch in other.children]
            and self.size == other.size
        )

    def __str__(self):
        basic_name = f"{self.name} {self.size} {self.node_type}"
        if self.children:
            appendix = " [{}]".format(", ".join(str(child) for child in self._children))
            basic_name += appendix

        return basic_name

    def __repr__(self):
        return str(self)


class FileTree:
    REGEX_CD = re.compile(r"^\$ cd (\S+)$")
    REGEX_LS = re.compile(r"^\$ ls$")
    REGEX_DIR = re.compile(r"^dir (\S+)$")
    REGEX_FILE = re.compile(r"^(\d+) (\S+)$")

    def __init__(self):
        self._root: FileNode = None
        self._current_node: FileNode = None

    def parse_input_row(self, input_row: str):
        if match := self.REGEX_CD.match(input_row):
            dir_name = match.group(1)
            if dir_name == "/" and self.root is None:
                self._root = FileNode("/")
                self._current_node = self._root
            elif dir_name == "..":
                if not getattr(self._current_node, "parent", None):
                    raise ValueError(f"Can't go .. from {self._current_node}")

                self._current_node = self._current_node.parent
            else:
                for child_dir in self._current_node.children:
                    if child_dir.name == dir_name:
                        self._current_node = child_dir
                        break
                else:
                    raise ValueError(
                        f"Can't go to dir {dir_name} from {self._current_node}"
                    )
        elif match := self.REGEX_LS.match(input_row):
            pass
        elif match := self.REGEX_DIR.match(input_row):
            dir_name = match.group(1)
            self._current_node.add_child(FileNode(dir_name))

        elif match := self.REGEX_FILE.match(input_row):
            file_name = match.group(2)
            file_size = int(match.group(1))
            self._current_node.add_child(FileNode(file_name, file_size))
        else:
            raise ValueError(f"Unexpected row pattern: {input_row}")

    @property
    def root(self):
        return self._root


class TestFileNode:
    def test_file_node_type(self):
        dir_ = FileNode("/")
        assert dir_.node_type == NodeType.FILE
        assert dir_.size == 0

        file_ = FileNode("file.name", 123)

        dir_.add_child(file_)
        assert dir_.node_type == NodeType.DIR
        assert file_.node_type == NodeType.FILE

    def test_file_node_parent(self):
        dir_ = FileNode("/")
        file_ = FileNode("file.name", 123, parent=dir_)

        assert file_ in dir_.children
        assert file_.parent == dir_

        dir_ = FileNode("/home")
        file_ = FileNode("file2.name", 200)
        dir_.add_child(file_)

        assert file_ in dir_.children
        assert file_.parent == dir_

    def test_file_node_dir_size(self):
        dir_ = FileNode("/")
        file_ = FileNode("file.name", 123, parent=dir_)

        assert dir_.size == 123

        file_2 = FileNode("file2.name", 200, parent=dir_)
        file_3 = FileNode("file3.name", 300, parent=dir_)

        assert dir_.size == 623

    def test_file_node_nested_dir_sizes(self):
        dir_ = FileNode("/")
        dir_2 = FileNode("dir2", parent=dir_)
        file_2 = FileNode("file2", 100, parent=dir_2)
        dir_3 = FileNode("dir3", parent=dir_2)
        file_31 = FileNode("file31", 200, parent=dir_3)
        file_32 = FileNode("file32", 300, parent=dir_3)

        assert dir_3.size == 500
        assert dir_2.size == 600
        assert dir_.size == 600

    def test_file_node_generate_dirs(self):
        dir_ = FileNode("/")
        dir_2 = FileNode("dir2", parent=dir_)
        file_2 = FileNode("file2", 100, parent=dir_2)
        dir_3 = FileNode("dir3", parent=dir_2)
        file_31 = FileNode("file31", 200, parent=dir_3)
        file_32 = FileNode("file32", 300, parent=dir_3)

        generated_dirs = list(dir_.generate_dirs())
        assert generated_dirs == [dir_, dir_2, dir_3]

    def test_file_node_disallows_same_file_names(self):
        dir_ = FileNode("/")
        file_ = FileNode("file.name", 123, parent=dir_)

        with pytest.raises(ValueError):
            FileNode(file_.name, 123, parent=dir_)

        assert len(dir_.children) == 1

        with pytest.raises(ValueError):
            dir_.add_child(FileNode(file_.name, 234))

        assert len(dir_.children) == 1


class TestFileTree:
    def test_file_tree_empty_dir(self):
        file_tree = FileTree()
        file_tree.parse_input_row("$ cd /")

        root = FileNode("/")
        assert str(file_tree.root) == str(root)

    def test_file_tree_dir_with_files(self):
        file_tree = FileTree()
        input_rows = [
            "$ cd /",
            "$ ls",
            "101350 gpbswq.njr",
            "270744 mglrchsr",
            "260405 qtvftbl",
        ]
        for input_row in input_rows:
            file_tree.parse_input_row(input_row)

        root = FileNode("/")
        leaves = [
            FileNode("gpbswq.njr", 101350, parent=root),
            FileNode("mglrchsr", 270744, parent=root),
            FileNode("qtvftbl", 260405, parent=root),
        ]

        root._children = leaves

        assert str(file_tree.root) == str(root)

    def test_file_tree_up_traversal(self):
        file_tree = FileTree()
        input_rows = [
            "$ cd /",
            "$ ls",
            "dir foo",
            "dir bar",
            "100 file1",
            "200 file2",
            "$ cd foo",
            "$ ls",
            "1000 file.foobar",
            "$ cd ..",
            "$ cd bar",
            "$ ls",
            "2000 file.barfoo",
        ]
        for input_row in input_rows:
            file_tree.parse_input_row(input_row)

        root = FileNode("/")
        foo = FileNode("foo", parent=root)
        bar = FileNode("bar", parent=root)
        root_children = [
            foo,
            bar,
            FileNode("file1", 100, parent=root),
            FileNode("file2", 200, parent=root),
        ]
        foo_children = [
            FileNode("file.foobar", 1000, parent=foo),
        ]
        bar_children = [
            FileNode("file.barfoo", 2000, parent=bar),
        ]

        assert foo.children == foo_children
        assert bar.children == bar_children
        assert str(file_tree.root) == str(root)


def main(input_file):
    TOTAL_SIZE = 70000000
    NEED_FREE = 30000000

    file_tree = FileTree()
    for line in input_file:
        file_tree.parse_input_row(line.strip())

    NEED_TO_DELETE = NEED_FREE - (TOTAL_SIZE - file_tree.root.size)
    dir_size_to_delete = TOTAL_SIZE

    for dir_ in file_tree.root.generate_dirs():
        if dir_.size >= NEED_TO_DELETE:
            dir_size_to_delete = min(dir_size_to_delete, dir_.size)

    print(dir_size_to_delete)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "07.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
