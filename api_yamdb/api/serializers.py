"""api_serializers."""
from rest_framework import serializers

from reviews.models import Category, Comment, Genres, Review, Title
from users.models import User

ERROR = 'К произведению можно оставлять не более одного обзора'


class ReviewSerializer(serializers.ModelSerializer):
    """ReviewSerializer."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        """ReviewSerializer_Meta."""
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        """ReviewSerializer_validate."""
        request = self.context['request']
        title_id = self.context['view'].kwargs['title_id']
        if (request.method == 'POST'
           and Review.objects.filter(author=request.user, title=title_id)):
            raise serializers.ValidationError(ERROR)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """CommentSerializer."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        """CommentSerializer_Meta."""
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)


class EmailSerializer(serializers.ModelSerializer):
    """EmailSerializer."""
    def validate(self, data):
        """EmailSerializer_validate."""
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" как юзернейм запрещено'
            )
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Юзернейм не уникален'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Email не уникален'
            )
        return data

    class Meta:
        """EmailSerializer_Meta."""
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    """TokenSerializer."""
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer."""
    class Meta:
        """."""
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """CategorySerializer."""
    class Meta:
        """Class_GroupSerializer_Meta."""
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """GenresSerializer."""
    class Meta:
        """GenresSerializer_Meta."""
        model = Genres
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    """TitlesReadSerializer."""
    category = CategorySerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """TitlesReadSerializer_Meta."""
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlesWriteSerializer(serializers.ModelSerializer):
    """TitlesWriteSerializer."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        read_only=False,
        queryset=Genres.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """TitlesWriteSerializer_Meta."""
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
