from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from demo.serializers import StudentModelSerializer
from stuapi.models import Student

"""APIView基本视图类"""


class StudentAPIView(APIView):
    def get(self, request):
        """获取所有学生信息"""
        # 1.从数据库中读取学生列表信息
        student_list = Student.objects.all()
        # 2.实例化序列化器，获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1.获取客户端提交的数据，实例化序列化器，获取序列化对象
        serializer = StudentModelSerializer(data=request.data)

        # 2.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoAPIView(APIView):
    def get(self, request, pk):
        """获取一条数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.序列化
        serializer = StudentModelSerializer(instance=student)
        # 3.返回结果
        return Response(serializer.data)

    def put(self, request, pk):
        """更新数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data)
        # 3.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """删除数据"""
        # 1.根据pk值获取要删除的数据并删除
        try:
            Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        # 2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericAPIView通用视图类"""


class StudentGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有模型信息"""
        # 1.从数据库中读取模型列表信息
        queryset = self.get_queryset()  # GenericAPIView提供的get_queryset
        # 2.序列化
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1.获取客户端提交的数据，实例化序列化器，获取序列化对象
        serializer = self.get_serializer(data=request.data)

        # 2.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        """获取一条数据"""
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2.序列化
        serializer = self.get_serializer(instance=instance)
        # 3.返回结果
        return Response(serializer.data)

    def put(self, request, pk):
        """更新一个数据"""
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2.获取客户端提交的数据
        serializer = self.get_serializer(instance=instance, data=request.data)
        # 3.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """删除一个数据"""
        # 1.根据pk值获取要删除的数据并删除
        instance = self.get_object().delete()
        # 2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
使用drf内置的模型扩展类[混入类]结合GenericAPIView实现通用视图方法的简写操作
"""
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class StudentMixinView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有数据"""
        return self.list(request)

    def post(self, request):
        """添加一条数据"""
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class StudentInfoMixinView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        """获取一条数据"""
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        """更新一个数据"""
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        """删除一个数据"""
        return self.destroy(request, pk=pk)


"""
视图子类是通用视图类和模型扩展类的子类，提供了各种的视图方法调用mixins操作
"""
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView


# class StudentView(ListAPIView, CreateAPIView):
class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


# class StudentInfoView(RetrieveAPIView, UpdateAPIView):
class StudentInfoView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
上面接口在实现过程中，也存在了代码重复的情况，我们如果合并成一个接口类，需要考虑2个问题：
1.路由的合并问题
2.get方法重复问题
"""
from rest_framework.viewsets import ViewSet


class StudentViewSet(ViewSet):
    def get_student_list(self, request):
        """获取所有学生信息"""
        # 1.从数据库中读取学生列表信息
        student_list = Student.objects.all()
        # 2.实例化序列化器，获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1.获取客户端提交的数据，实例化序列化器，获取序列化对象
        serializer = StudentModelSerializer(data=request.data)

        # 2.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_student_info(self, request, pk):
        """获取一条数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.序列化
        serializer = StudentModelSerializer(instance=student)
        # 3.返回结果
        return Response(serializer.data)

    def update(self, request, pk):
        """更新数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data)
        # 3.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """删除数据"""
        # 1.根据pk值获取要删除的数据并删除
        try:
            Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        # 2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericAPIView通用视图类"""
from rest_framework.viewsets import GenericViewSet


class StudentGenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def list(self, request):
        """获取所有模型信息"""
        # 1.从数据库中读取模型列表信息
        queryset = self.get_queryset()  # GenericAPIView提供的get_queryset
        # 2.序列化
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def create(self, request):
        """添加一条数据"""
        # 1.获取客户端提交的数据，实例化序列化器，获取序列化对象
        serializer = self.get_serializer(data=request.data)

        # 2.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        """获取一条数据"""
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2.序列化
        serializer = self.get_serializer(instance=instance)
        # 3.返回结果
        return Response(serializer.data)

    def update(self, request, pk):
        """更新一个数据"""
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2.获取客户端提交的数据
        serializer = self.get_serializer(instance=instance, data=request.data)
        # 3.反序列化【验证数据、保存数据到数据库】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """删除一个数据"""
        # 1.根据pk值获取要删除的数据并删除
        instance = self.get_object().delete()
        # 2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
GenericViewSet 通用视图集+混入类
ReadOnlyModelViewSet = mixins.RetrieveModelMixin + mixins.ListModelMixin + GenericViewSet
ModelViewSet
实现5个API接口
"""
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action


class StudentReadOnlyMixinViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # action自动生成路由信息，detail为true表示有pk值,url_path设置路由
    @action(methods=["put"], detail=False, url_path="login")
    def login(self, request):
        """登录视图"""
        username = request.data.get('username')
        password = request.data.get('password')
        print(1, username, password)
        if username == "dpp1" and password == "123":
            return Response({"msg": "登陆成功"})
        else:
            return Response({"msg": "登陆失败"})
        # return Response({"msg": "登陆成功"})
