from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #保存了所有的HTTP响应状态码

# 原生
class StudentView(View):
    def get(self, request):
        print(f"request={request}")
        return HttpResponse("ok")


class StudentAPIView(APIView):
    def get(self, request):
        print(f"drf.request={request}")
        """获取查询参数/查询字符串"""
        print(f"request.query_params={request.query_params}")
        return Response({"msg", "ok"}, status=status.HTTP_201_CREATED, headers={"Company": "Django"})

    def post(self, request):
        # 添加数据
        # 获取请求体数据
        print(f"request.data={request.data}")  # 接受的数据已经被Parse解析器转换成字典数据了
        """获取查询参数/查询字符串"""
        print(f"request.query_params={request.query_params}")
        return Response({"msg", "ok"})

    def put(self, request):
        # 更新数据
        return Response({"msg", "ok"})

    def patch(self, request):
        # 更新数据【部分】
        return Response({"msg", "ok"})

    def delete(self, request):
        # 删除数据【部分】
        return Response({"msg", "ok"})
