import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.six import BytesIO
#
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from rest_framework.utils import json
from tqdm import tqdm

from chat_admin.models import DishInfo

from chatBot.dish_graph import dishGraph
from chatBot.ModelProcess import ModelProcess
from chatBot.qa import get_response

# from chat_admin.serializers import UserInfoSerializer, TestDataSerializer

# Create your views here.
chatbot = None
if chatbot == None:
    chatbot = ModelProcess()
print("qa systerm load success")

dish_list = []


@csrf_exempt
def test_print(request):
    return HttpResponse("hello world")


@csrf_exempt
def user_chat(request):
    if request.method == "POST":
        question = request.POST.get("question", None)
        m = chatbot.analyQuery(question)
        dish_name = m.split(' ')[0]
        try:
            if chatbot.modelIndex < 4:
                a = get_response(chatbot.modelIndex, dish_name)
                print(a)
            elif chatbot.modelIndex == 4:
                dish_list.append(dish_name)
                a = dish_name + "已加入菜单,当前已点菜为：" + '、'.join(dish_list)
            elif chatbot.modelIndex == 5:
                dish_list.remove(dish_name)
                a = dish_name + "已移出菜单,当前已点菜为：" + '、'.join(dish_list)
            else:
                a = "抱歉，请再说一次"
        except:
            a = "抱歉，请再说一次"
            print("抱歉，请再说一次")
        print(a)
        return HttpResponse(a)
    return render(request, "chatPage.html")


def get_answer(answer):
    HttpResponse(answer)


def index(request):
    dish_list = DishInfo.objects.all()
    if request.method == "POST":
        name = request.POST.get("name", None)
        type = request.POST.get("type", None)
        content = request.POST.get("content", None)
        price = request.POST.get("price", None)
        rating = request.POST.get("rating", None)
        DishInfo.objects.create(u_name=name, u_type=type, u_content=content, u_price=price, u_rating=rating)
        print(name, type, content, price, rating)
    return render(request, "index.html", {"data": dish_list})


def delete_item(request):
    name = request.path_info.split('/')[-1]
    dish_list = DishInfo.objects.all()
    try:
        dish = DishInfo.objects.get(u_name=name)
    except DishInfo.DoesNotExist:
        return render(request, "index.html", {"data": dish_list})
    dish.delete()
    return render(request, "index.html", {"data": dish_list})


# 构建知识图谱
def create_KnowledgeGraph(request):
    graph = dishGraph()
    graph.delete(pattern='all')
    for dish in DishInfo.objects.all():
        graph.add_Dish_Cell(name=dish.u_name, type=dish.u_type, content=dish.u_content, price=dish.u_price,
                            rating=dish.u_rating)

    print("知识图谱生成成功")
    return render(request, "index.html", {"data": DishInfo.objects.all()})


import xlrd
import string


def test_add_dishlist(request):
    data = xlrd.open_workbook('./chatBot/dish.xlsx')
    table = data.sheet_by_index(0)
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
                try:
                    dish = DishInfo.objects.get(u_name=name)
                except DishInfo.DoesNotExist:
                    DishInfo.objects.create(u_name=name, u_type=type, u_content=content, u_price=price, u_rating=rating)
        except:
            print("error")
    return render(request, "index.html", {"data": DishInfo.objects.all()})
