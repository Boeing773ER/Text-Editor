from pyecharts import options as opts
from pyecharts.charts import Tree
from Structure import *


def generate_data(huff_tree):
    if huff_tree is None:
        return False
    else:
        data = list()
        data.append(insert_node(huff_tree.root))
        return data


def insert_node(tree_node):
    if tree_node is not None:
        temp_dict = dict()
        temp_list = list()
        if tree_node.left is not None:
            temp_list.append(insert_node(tree_node.left))
            temp_list.append(insert_node(tree_node.right))
            temp_dict['children'] = temp_list
            temp_dict['name'] = tree_node.value
        else:
            temp_dict['value'] = tree_node.code
            temp_dict['name'] = '\'' + tree_node.name + '\': ' + tree_node.code
        return temp_dict


def gen_huff_tree(huff_a):
    data_a = generate_data(huff_a)      # generate data for Print tree
    # for debug
    # print(type(huff_a.root.right.right.right.code))
    c = (
        Tree()
            .add("", data_a)
            .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
            .render("tree_base.html")
    )
    return gen_huff_code(huff_a)


def gen_huff_code(huff_tree):
    dict_a = dict()
    huff_tree.to_dict(huff_tree.root, dict_a)
    return dict_a

