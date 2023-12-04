from rest_framework.serializers import ModelSerializer
from libreria.models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']
