"""views."""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination,
)
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.filters import TitleFilter
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly, IsModeratorOrAdminOrAuthor,
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenresSerializer, ReviewSerializer,
    TitlesReadSerializer, TitlesWriteSerializer, UserSerializer,
)
from reviews.models import Category, Genres, Review, Title
from users.models import User


class GenreAndCategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """GenreAndCategoryViewSet."""

    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """ReviewViewSet."""
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsModeratorOrAdminOrAuthor)
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_title(self):
        """ReviewViewSet_get_title."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """ReviewViewSet_get_queryset."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """ReviewViewSet_perform_create."""
        serializer.save(
            author=self.request.user,
            title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """CommentViewSet."""
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsModeratorOrAdminOrAuthor)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_review(self):
        """CommentViewSet_get_review."""
        return get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """CommentViewSet_get_queryset."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """CommentViewSet_perform_create."""
        serializer.save(
            author=self.request.user,
            review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """UserViewSet."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """UserViewSet_me."""
        user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.is_user or request.user.is_moderator:
                    serializer.save(role=user.role)
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(GenreAndCategoryViewSet):
    """CategoryViewSet."""
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(GenreAndCategoryViewSet):
    """GenresViewSet."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """TitlesViewSet."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """TitlesViewSet_get_serializer_class."""
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer
