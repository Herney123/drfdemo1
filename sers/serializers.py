from rest_framework import serializers


class BookModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    price = serializers.IntegerField()
    pub_date = serializers.DateField()
    publish_id = serializers.IntegerField(write_only=True)
    publish_name = serializers.CharField(source="publish.name", read_only=True)
    publish_email = serializers.CharField(source="publish.email", read_only=True)