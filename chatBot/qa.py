__author__ = 'ding'
'''
qa问答
'''
from .ModelProcess import ModelProcess
from .dish_graph import dishGraph

graph = dishGraph()


# 构建知识图谱
def create_Knowledge_Graph():
    graph.delete(pattern='all')
    graph.handle_excel('./dish.xlsx', ['Sheet1'])


# create_Knowledge_Graph()

# 获取回复
def get_response(index, dish_name):
    # self.graph.run("MATCH(n:" + type + ") Where n.{} n")

    if index < 5:
        label = 'Dish'
    else:
        label = 'person'

    # 类别
    value = ['rating', 'type', 'content', 'price']
    node = graph.selector.match(label).where(name=dish_name).first()

    return node[value[index]]


# qa = ModelProcess()
# # qa.queryAbstract(question)
# while 1:
#     question = input('>')
#     m = qa.analyQuery(question)
#     dish_name = m.strip().split(' ')[0]
#     try:
#         if qa.modelIndex == 4:
#             global dish_list
#             dish_list.append(dish_name)
#             print(dish_name + " 已加入列表")
#             print("当前已点菜：" + ' '.join(dish_list))
#         elif qa.modelIndex == 5:
#             dish_list.remove(dish_name)
#             print(dish_name + "已移除")
#             print("当前已点菜：" + ' '.join(dish_list))
#         else:
#             a = get_response(qa.modelIndex, dish_name)
#             print(a)
#     except:
#         print("抱歉，请再说一次")
