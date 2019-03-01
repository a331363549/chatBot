from django.db import models
from markdown import serializers
from pygments.lexers import get_all_lexers  # 一个实现代码高亮的模块
from pygments.styles import get_all_styles

# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  # 得到所有编程语言的选项
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())  # 列出所有配色风格


# Create your models here.

class DishInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    u_name = models.CharField('菜名', max_length=11)
    u_type = models.CharField('类别', max_length=20, null=True, blank=True)
    u_content = models.CharField('简介', max_length=200, null=True, blank=True)
    u_price = models.IntegerField('价格', null=True, blank=True)
    u_rating = models.IntegerField('评分')

    def __str__(self):
        return self.u_name

    class Meta:
        ordering = ('created',)
