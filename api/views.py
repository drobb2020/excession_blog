from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from a_blog.models import Post
from a_services.models import Review

from .serializers import PostSerializer, ReviewSerializer


@api_view(["GET"])
def getRoutes(request):

    routes = [{"GET": "/api/posts"}, {"GET": "/api/posts/id"}]

    return Response(routes)


@api_view(["GET"])
def getPosts(request):
    print('USER:', request.user)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getReviews(request):
    print("USER:", request.user)
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getReview(request, pk):
    review = Review.objects.get(id=pk)
    serializer = ReviewSerializer(review, many=False)
    return Response(serializer.data)
