from typing import Union
import os
import json


class Node:
    def __init__(self, name, value=None, parent=None, children: list = None, metadata: dict = None):
        if parent:
            if not isinstance(parent, Node):
                raise TypeError("parent type must be <class Node>")
        if children:
            if not isinstance(children, list):
                raise TypeError("children type must be <class list>")
        if metadata:
            if not isinstance(metadata, dict):
                raise TypeError("metadata type must be <class dict>")
        self.name = name
        self.value = value
        self.parent = parent
        self.metadata = metadata if metadata else []
        self.children = children if children else []
        if self.parent is not None:
            self.parent.add_child(self)

    def add_child(self, node_1):
        self.children.append(node_1)


class Tree:
    tree_types = ['json', 'xml']

    def __init__(self, root):
        if not isinstance(root, Node):
            raise TypeError("root type must be <class Node>")
        self.__root = root
        self.__item = None
        self.__data_json = {}
        self.__key_path = []
        self.__data_xml = ''
        self.__index = None
        self.__depth = 4

    def write(self, path, data_format):
        if data_format not in Tree.tree_types:
            raise ValueError(f"data has {Tree.tree_types} formats, no {data_format}")
        with open(os.path.normpath(path), 'a') as file:
            if data_format == 'json':
                json.dump(self.get_json_format(), file)
            else:
                file.write(self.get_xml_format())

    def get_json_format(self) -> dict:  # xml_to_json
        if self.__data_json:
            return self.__data_json
        self.__node_to_json()
        return self.__data_json

    def get_xml_format(self, wrap: str = 'data') -> str:  # json_to_xml
        if self.__data_xml:
            return self.__data_xml
        self.__data_xml = f"<{wrap}>\n\t\n</{wrap}>".expandtabs(self.__depth)
        self.__node_to_xml()
        return self.__data_xml

    def __node_to_xml(self):
        data = self.__item.children if self.__item else self.__root.children
        for i, item in enumerate(data):
            index = self.__data_xml.find('\n ', self.__index if self.__index else 0)
            if item.value is not None:
                detail = '\n\t' if i != len(data) - 1 else ''
                if not item.metadata:
                    self.__data_xml = \
                        f"{self.__data_xml[:index + self.__depth + 1]}<{item.name}>{item.value}" \
                        f"</{item.name}>{detail}{self.__data_xml[index + self.__depth + 1:]}".expandtabs(self.__depth)
                else:
                    self.__data_xml = \
                        f"{self.__data_xml[:index + self.__depth + 1]}<{item.name} id={item.metadata['id']}>" \
                        f"{item.value}</{item.name}>{detail}{self.__data_xml[index + self.__depth + 1:]}".expandtabs(
                            self.__depth)
                self.__index = index + self.__depth + 1
            else:
                info = f" id={item.metadata['id']}" if item.metadata else ''
                detail = '\n\t\n' if i != len(data) - 1 else '\n'
                detail_ = f"{self.__data_xml[:index + self.__depth + 1]}<{item.name}{info}>\n\t".expandtabs(
                    self.__depth + 4)
                detail__ = f"\n\t</{item.name}>{detail}{self.__data_xml[index + self.__depth + 2:]}".expandtabs(
                    self.__depth)
                self.__data_xml = f'{detail_}{detail__}'

                self.__index = index + self.__depth + 1
                self.__depth += 4
                self.__item = item
                self.__node_to_xml()
                self.__index = self.__data_xml.find('\n ', self.__index if self.__index else 0) + 1
                self.__depth -= 4
                self.__item = None

    def __node_to_json(self):
        data = self.__data_json
        for key in self.__key_path:
            data = data[key]
        for item in self.__item.children if self.__item else self.__root.children:
            name = item.name.strip('_sub')
            if item.value is not None:
                if isinstance(data, dict):
                    data.update({name: item.value})
                else:
                    data.append(item.value)
            else:
                if isinstance(data, dict):
                    data.update({name: [] if item.children[0].metadata else {}})
                else:
                    data.append([] if item.children[0].metadata else {})
                self.__key_path.append(int(item.metadata['id']) - 1 if item.metadata else name)
                self.__item = item
                self.__node_to_json()
                self.__key_path = self.__key_path[:-1]
                self.__item = None

    @staticmethod
    def build_tree(data: Union[str, dict], data_format):
        if not isinstance(data, (str, dict)):
            raise TypeError(f"data type must be {str, dict}")
        if data_format not in Tree.tree_types:
            raise ValueError(f"data has {Tree.tree_types} formats, no {data_format}")
        try:
            if data_format == 'json':
                data = str(data)
                data_types = {
                    'false': False,
                    'true': True,
                    'undefined': None,
                    'null': None
                    # todo
                }
                for key, value in data_types.items():
                    data.replace(key, str(value))
                # try:
                #     data = eval(data)
                # except Exception as e:
                #     raise Exception(e)
                data = eval(data)
                root = Node('data')
                Tree.json_to_node(data, root)
                return Tree(root)
            else:
                list_data = list(map(lambda x: x.strip(), filter(lambda x: True if x else False, data.split('\n'))))
                return Tree(Tree.xml_to_node(list_data))
        except Exception:
            raise ValueError('Check values')

    @staticmethod
    def xml_to_node(list_data: list, root=None):
        for i, item in enumerate(list_data):
            ind = item.find('<') + 1
            ind_ = item.find(' id=')
            ind__ = item.find('>')
            ind___ = item.find('</')
            name = item[ind:ind_ if ind_ != -1 else ind__]
            if '</' in item:
                node = Node(name, parent=root,
                            metadata={'id': int(item[ind_ + 4])} if ind_ != -1 else {}, value=item[ind__ + 1:ind___])
            else:
                node = Node(name, parent=root,
                            metadata={'id': int(item[ind_ + 4])} if ind_ != -1 else {})
                end = list_data.index(f"</{name}>", i)
                Tree.xml_to_node(list_data[i + 1:end], node)
                del list_data[i:end]
            root_ = node
        return root_

    @staticmethod
    def json_to_node(data: dict, root):
        if isinstance(data, dict):
            data = data.items()
            flag = False
        else:
            data = enumerate(data)
            flag = True
        if not root.name.endswith('_sub') and root.name.endswith(r'_id_\d'):
            info = '{}'
        else:
            if root.metadata and flag:
                info = f'{root.name}_id_{root.metadata["id"]}'
            else:
                info = 'sub_{}'
        for key, value in data:
            metadata = {}
            if isinstance(data, enumerate):
                metadata = {'id': key + 1}
            if isinstance(value, dict):
                root_ = Node(info.format(key), parent=root, metadata=metadata)
                Tree.json_to_node(value, root_)
                continue
            if isinstance(value, list):
                root_ = Node(info.format(key), parent=root)
                for i, item in enumerate(value):
                    if isinstance(item, (dict, list)):
                        node = Node(f'{info.format(key)}_sub', parent=root_, metadata={'id': i + 1})
                        Tree.json_to_node(item, node)
                        continue
                    Node(f'{info.format(key)}_sub', parent=root_, metadata={'id': i + 1}, value=item)
                continue
            Node(info.format(key), parent=root, value=value, metadata=metadata)


if __name__ == '__main__':
    string = open('f.xml', 'r').read()
    d = {'data_1': 1,
         'data_2': [[{"a": [[3, 2], {1: 21}]}, 5, 6], 2, 5],
         'data_3': {'sub_d_1': 3,
                    'sub_d_2': 5}
         }
    e = {'data_1': 1,
         'data_2': [1, 2, 5],
         'data_3': {'sub_d_1': 3,
                    'sub_d_2': 5}
         }
    T = Tree.build_tree(string, data_format='xml')
    # print(T._Tree__root.children[1].children[0].children[0].metadata)

    print(T.get_xml_format())
    print(T.get_json_format())
