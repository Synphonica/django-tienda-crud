from rest_framework.viewsets import ModelViewSet
from libreria.models import Post
from libreria.api.serializer import PostSerializer

class PostApiViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()