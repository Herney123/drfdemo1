from rest_framework import serializers
from stuapi.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {
            "age": {
                "max_value": 25,
                "error_messages": {
                    "max_value": "年龄不能超过25岁！",
                }
            }
        }
