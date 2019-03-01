import xlrd
from tqdm import tqdm

__author__ = 'ding'
'''

'''
import string
from py2neo import Graph, Node, Relationship, NodeMatcher


class dishGraph:
    def __init__(self, password="123"):
        self.rdb = None
        self.graph = Graph("http://localhost:7474/db/data", password=password)
        self.selector = NodeMatcher(self.graph)

    # 菜品节点
    def add_Dish_Cell(self, label='Dish', name=None, type='', content='', price='', rating=''):
        assert name is not None
        # self.add_Dish_Cell(name=name, type=type, content=content, price=price,
        #                    rating=rating)
        node = self.selector.match('Dish').where(name=name).first()
        with open('./dish.txt', 'a', encoding='utf-8') as fw:
                fw.write(name + " nz\n")
        if node:
            node['name'] = name
            node['type'] = type
            node['content'] = content
            node['price'] = price
            node['rating'] = rating
            self.graph.push(node)
        else:
            node = Node(label, name=name, type=type, content=content, price=price, rating=rating)
            self.graph.create(node)
            # for genre in genres.split('|'):
            #     node_genre = self.selector.match('Genre').where(genre=genre).first()
            #     if node_genre:
            #         g_r_n = Relationship(node, 'is', node_genre)
            #     else:
            #         node_genre = Node('Genre', genre=genre)
            #         self.graph.create(node_genre)
            #         g_r_n = Relationship(node, 'is', node_genre)
            #     self.graph.create(g_r_n)
            # for actor in actors.split('|'):
            #     node_actor = self.selector.match('Person').where(name=actor).first()
            #     if node_actor:
            #         a_r_n = Relationship(node, 'acting', node_actor)
            #     else:
            #         node_actor = Node('Person', name=actor)
            #         self.graph.create(node_actor)
            #         a_r_n = Relationship(node, 'acting', node_actor)
            #     self.graph.create(a_r_n)

    # 电影种类节点
    def add_Movie_Genre(self, label='Genre', genre=None, movie=""):
        assert genre is not None
        node = self.selector.match('Genre').where(genre=genre).first()
        if node:
            node['genre'] = genre
            self.graph.push(node)
        else:
            node = Node(label, genre=genre)
            self.graph.create(node)
        node_movie = self.selector.match('Movie').where(name=movie).first()
        assert node_movie is not None
        node_r_movie = Relationship(node, 'is', node_movie)
        self.graph.create(node_r_movie)

    # 人物信息节点
    def add_Person_Cell(self, label='Person', name=None, borndata='', desc='', movie=''):
        assert name is not None
        node = self.selector.match('Person').where(name=name).first()
        if node:
            node['name'] = name
            node['borndata'] = borndata
            node['desc'] = desc
            self.graph.push(node)
        else:
            node = Node(label, name=name, borndata=borndata, desc=desc)
            self.graph.create(node)
        node_movie = self.selector.match('Movie').where(name=movie).first()
        assert node_movie is not None
        node_r_movie = Relationship(node, 'acting', node_movie)
        self.graph.create(node_r_movie)

    def delete(self, pattern="n", label=None):
        """Batch delete data or subgraph in database.
        在数据库中批量删除数据或者子图。

        Args:
            pattern: Type of subgraph. 子图类型。
            label: Label of subgraph. 子图标签。
        """
        if pattern == "all":
            self.graph.delete_all()
        elif pattern == "n":
            self.graph.run("MATCH(n:" + label + ") DETACH DELETE n")
        elif pattern == "r":
            self.graph.run("MATCH (n)-[r:" + label + "]-(m) DETACH DELETE r")
        elif pattern == "nr":
            self.graph.run("MATCH (n)<-[r:" + label + "]-(m) DETACH DELETE r, n")
        elif pattern == "rm":
            self.graph.run("MATCH (n)-[r:" + label + "]->(m) DETACH DELETE r, m")
        elif pattern == "nrm":
            self.graph.run("MATCH (n)-[r:" + label + "]-(m) DETACH DELETE r, n, m")

    def handle_excel(self, filename=None, custom_sheets=[]):
        assert filename is not None
        data = xlrd.open_workbook(filename)
        data_sheets = data.sheet_names()
        if custom_sheets:  # 可自定义要导入的子表格
            sheet_names = list(set(data_sheets).intersection(set(custom_sheets)))
        else:
            sheet_names = data_sheets
        for sheet_name in sheet_names:
            table = data.sheet_by_name(sheet_name)
            if table:
                col_format = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                try:
                    nrows = table.nrows
                    str_upcase = [i for i in string.ascii_uppercase]
                    i_upcase = range(len(str_upcase))
                    ncols_dir = dict(zip(str_upcase, i_upcase))
                    col_index = [ncols_dir.get(i) for i in col_format]
                    for i in tqdm(range(1, nrows)):
                        name = table.cell_value(i, col_index[0])
                        type = table.cell_value(i, col_index[1])
                        content = table.cell_value(i, col_index[2])
                        price = table.cell_value(i, col_index[3])
                        rating = table.cell_value(i, col_index[4])

                        # for actor in actors.split('|'):
                        #     self.add_Person_Cell(name=actor, movie=name)
                        self.add_Dish_Cell(name=name, type=type, content=content, price=price,
                                           rating=rating)
                except Exception as error:
                    print('Error: %s' % error)
                    return None
