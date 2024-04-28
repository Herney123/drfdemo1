from django.urls import path, re_path
from . import views

urlpatterns = [
    # APIView
    path("students/", views.StudentAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", views.StudentInfoAPIView.as_view()),

    # GenericAPIView
    path("students2/", views.StudentGenericAPIView.as_view()),
    re_path("^students2/(?P<pk>\d+)/$", views.StudentInfoGenericAPIView.as_view()),

    # GenericAPIView + mixins
    path("students3/", views.StudentMixinView.as_view()),
    re_path("^students3/(?P<pk>\d+)/$", views.StudentInfoMixinView.as_view()),

    # 视图子类
    path("students4/", views.StudentView.as_view()),
    re_path("^students4/(?P<pk>\d+)/$", views.StudentInfoView.as_view()),

    # 视图集：ViewSet
    path("students5/", views.StudentViewSet.as_view({
        "get": "get_student_list",  # 视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        "post": "post",
    })),
    re_path("^students5/(?P<pk>\d+)/$", views.StudentViewSet.as_view({
        "get": "get_student_info",
        "put": "update",
        "delete": "delete",
    })),
    # 视图集：GenericViewSet
    path("students6/", views.StudentGenericViewSet.as_view({
        "get": "list",  # 视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        "post": "create",
    })),
    re_path("^students6/(?P<pk>\d+)/$", views.StudentGenericViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    })),
    # 视图集：ReadOnlyModelViewSet
    path("students7/", views.StudentReadOnlyMixinViewSet.as_view({
        "get": "list",  # 视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        "post": "create",
    })),
    re_path("^students7/(?P<pk>\d+)/$", views.StudentReadOnlyMixinViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    })),
    # 视图集：ModelViewSet
    path("students8/", views.StudentModelViewSet.as_view({
        "get": "list",  # 视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        "post": "create",
    })),
    re_path("^students8/(?P<pk>\d+)/$", views.StudentModelViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    })),

]

# 自动生成路由信息【和视图集一起使用】
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1.实例化路由类
router = DefaultRouter()
# 2.给路由去注册视图集
router.register("students9", views.StudentModelViewSet, basename="students9")
# 3.把生成的路由列表和urlpatterns进行拼接
urlpatterns += router.urls
