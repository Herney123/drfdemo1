from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# 原生代码提供api接口
from django.views import View

from stuapi.models import Student


class StudentView(View):
    def post(self, request):
        # 添加一个学生信息
        # 接受客户端提交的数据，验证客户端的数据
        name = request.POST.get("name")
        sex = request.POST.get("sex")
        age = request.POST.get("age")
        class_null = request.POST.get("class_null")
        description = request.POST.get("description")
        # 操作数据库保存数据
        instance = Student.objects.create(
            name=name,
            sex=sex,
            age=age,
            class_null=class_null,
            description=description,

        )
        # 返回结果
        return JsonResponse(data={
            "id": instance.pk,
            "name": instance.name,
            "sex": instance.sex,
            "age": instance.age,
            "class_null": instance.class_null,
            "description": instance.description,
        }, status=201)
