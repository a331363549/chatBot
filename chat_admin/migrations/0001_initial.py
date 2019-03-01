# Generated by Django 2.1.7 on 2019-02-22 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DishInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('u_name', models.CharField(max_length=11, verbose_name='菜名')),
                ('u_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='类别')),
                ('u_content', models.CharField(blank=True, max_length=200, null=True, verbose_name='简介')),
                ('u_price', models.IntegerField(blank=True, null=True, verbose_name='价格')),
                ('u_rating', models.IntegerField(verbose_name='评分')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]