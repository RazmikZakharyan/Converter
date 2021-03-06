# json-xml-converter

Homework consist of two parts: <br>

To know more about xml data <br>
https://www.w3schools.com/xml/xml_whatis.asp <br>
More abiout json <br>
https://www.w3schools.com/js/js_json_intro.asp <br>

We will consider XML files withot single self closed tags and metadata should be only id so it will indicates list data type.<br>

1. First part is to create module that would conver json data to xml and vice versa. <br>
2. create command which takes json or xml file and convert it to xml or json file and save as file <br>
<br>
Coverter module <br>
Have following classes <br>

1. Node 
2. Tree

Node has following attributes <br>
-parent type Node if parent is none then it is root <br>
-name type string(this is for xml tag names and for json keywords <br>
-value type string(this is data between tags or value of key for json <br>
-metadata type dict -- used to indicate strings in xml giving them id <br>
-childs type list of nodes <br>

```def __init__(self,name, value=None, parent=None,childs=[])``` <br>
if paretn is not None init adds created instance to parent's childs list <br><br>

```def add_child(self, node_1)``` - appends node_1 too node's childs <br>

class Tree hass following attributes <br>
<br>
root type Node <br>
tree_type choices -- {'xml', 'json'}  <br>
<br>
use ```def xml_to_json(self)``` to convert xml to json <br>

use ```def json_to_xml(self)``` to convert json to xml <br>

```def write(self, path):``` writes converted data to path <br>

```def result(self)``` returns converted xml string or converted json dict <br>

```def build_tree(data)``` class method, gets xml or json data and creates corresponding nodes and returns tree <br>

result function calls json_to_xml or xml_to_json depends on Tree type and returns result  <br>

write function writes result to coresponding file <br><br>


EXAMPLES: <br>
we have following json data 
```
{'data_1': 1,
  'data_2': [1, 2, 5],
  'data_3': {'sub_d_1': 3,
             'sub_d_2': 5}
  }
```

We should have nodes as follow <br>
because json don't have root we can create <br>
```
root = Node('data') 
node_1 = Node('data_1', parent=root, value=1)
node_2 = Node('data_2', parent=root)
``` 
<br>
for list we createing subnodes with metadata id <br>

```
sub_node2_1 = Node('data_2_sub',parent=node_2, metadata={'id': 0}, value=1)
sub_node2_2 = Node('data_2_sub',parent=node_2, metadata={'id': 1}, value=2)
sub_node2_3 = Node('data_2_sub',parent=node_2, metadata={'id': 2}, value=5)
node_3 = Node('data_3', parent=root)
sub_node3_1 = Node('sub_d_1', parent=node_3, value=3)
sub_node3_2 = Node('sub_d_2', parent=node_3, value=5)
```

to create Tree we should do <br>

```tree = Tree(root, type=json)```

to convert from json to xml we use tree preorder traversals that means paretn first reading <br>
<br>
so for our example we read root data and write coresponding tag in string ```"<data>\n {} \n</data>"```,  <br>
if node doesn't have childs we write data instead of {} <br>
if node has childs for each child we doing same thing as we did for root <br>
in our example next we will have ```"<data>\n <data_1> 1 < /data_1> \n {} \n</data>"```, <br>
then  ```"<data>\n <data_1> 1 < /data_1> \n <data_2>\n {} </data_2> {}\n</data>"```,<br>
then ```"<data>\n <data_1> 1 < /data_1> \n <data_2>\n <data_2_sub id=0 > 1 </data_2_sub> \n {} </data_2> {} \n</data>"```,<br>
  .... etc
  
if we have following xml data

```
<data>
  <data_1>2</data_1>
  <data_2> 
    <data_2_sub id=1>2</data_2_sub>
    <data_2_sub id=2>4</data_2_sub>
  </data_2>
  <data_3>
    <data_4>
      <d41>String1</d41>
      <d42>154</d42>
    </data_4>
    <data_5>123</data_5>
  </data_3>
</data> 
```
converted json should be
```
{"data_1": 2,
 "data_2": [2, 4],
 "data_3": { "data_4": {"d41" :"String1", "d42": 154}, "data_5": 123}
 }
 ```
 
Command 
1. write command that have at least following instructions:

```
usage: xml-json-converter [-h] [-m {output,path}]
                          path_to_data [path_to_convert]

This command convert from json data type to xml and vice versa. path_to_data
is required argument it indicate path of file that should be converted.
path_to_convert indicates path of file where should be saved converted data if
mode is path

positional arguments:
  path_to_data          path to file to be converted
  path_to_convert       path to file to be saved converted data

optional arguments:
  -h, --help            show this help message and exit
  -m {output,path}, --mode {output,path}
                        if mode is path then path_to_convert is required,
                        converted data should be saved in path_to_convert
                        file,if mode is print converted data should be printed
                        in console.
```
This command uses converter that you created from the first part of homework
