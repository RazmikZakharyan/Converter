import argparse
import json
import os
from JsonXmlConverter import Tree

description = "This command convert from json data type to xml and vice versa. path_to_data" \
              "is required argument it indicate path of file that should be converted. " \
              "path_to_convert indicates path of file where should be saved converted data if mode is path"

parser = argparse.ArgumentParser(prog='converter',
                                 description=description,
                                 usage='json-xml-converter [-h] [-m {output,path}] '
                                       'path_to_data [path_to_convert]'
                                 )
parser.add_argument('path_to_data', type=str, help='path to file to be converted')
parser.add_argument('path_to_convert', type=str, help='path to file to be saved converted data')
parser.add_argument('-m', '--mode', choices=['output', 'path'], default='output',
                    help="if mode is path then path_to_convert is required,"
                         "converted data should be saved in path_to_convert"
                         "file, if mode is print converted data should be printed"
                         "in console.")

args = parser.parse_args()

with open(os.path.normpath(args.path_to_data), 'r') as file:
    suffixes = os.path.splitext(args.path_to_data)[1][1:]
    if suffixes == 'json':
        data = json.load(file)
        tree = Tree.build_tree(data, data_format='json')
    elif suffixes == 'xml':
        data = file.read()
        tree = Tree.build_tree(data, data_format='xml')
    else:
        raise Exception('suffixes error')

suffixes = 'json' if suffixes != 'json' else 'xml'

data = getattr(tree, f'get_{suffixes}_format')()

if args.mode == 'output':
    print(data)
elif args.mode == 'path':
    with open(os.path.normpath(args.path_to_convert), 'w') as file:
        if suffixes == 'json':
            json.dump(data, file)
        else:
            file.write(data)
