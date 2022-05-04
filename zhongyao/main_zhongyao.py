# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2022/4/28 8:17

    project name:Knowlegde_Graph_TCM
    file name:main_zhongyao.py
    function:
        中药知识图谱demo
"""
import json
from py2neo import Graph, Node, Relationship


def generateGraph_Node(graph, label, name):
    """
        创建知识图谱节点
    :param graph: Graph()
    :param label: 节点label
    :param name: 节点name
    :return:
    """

    node = Node(label, name=name)
    graph.create(node)

    return node


def generateGraph_Relation(graph, node_1, relation, node_2):
    """
        连接知识图谱关系
    :param graph:Graph()
    :param node_1: 头实体节点
    :param relation: 关系
    :param node_2: 尾实体节点
    :return:
    """

    r = Relationship(node_1, relation, node_2)
    graph.create(r)


def create_graph_zhongyao():
    """
        创建中药知识图谱，在neo4j中进行可视化
    :return:
    """

    # === 连接知识图谱
    connect_graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))

    # === 加载节点数据,创建节点
    # 创建关系时索引节点
    dict_nodes = {}  # key: 节点lable\tname, value:生成的图节点
    with open("./data_zhongyao/nodes_zhongyao.txt", "r", encoding="utf-8") as fr_n:
        for line in fr_n.readlines():
            line = line.strip()
            lable, name = line.split("\t")
            # 创建节点
            node = generateGraph_Node(connect_graph, lable, name)
            dict_nodes[line] = node

    # === 加载关系数据
    with open("./data_zhongyao/relations_zhongyao.json", "r", encoding="utf-8") as fr_r:
        for ele in json.load(fr_r):
            node_1 = ele["node_1"]
            relation = ele["relation"]
            node_2 = ele["node_2"]
            node_1_g = dict_nodes[node_1]
            node_2_g = dict_nodes[node_2]
            # 创建关系
            generateGraph_Relation(connect_graph, node_1_g, relation, node_2_g)


if __name__ == '__main__':
    create_graph_zhongyao()
    pass