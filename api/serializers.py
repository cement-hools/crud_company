from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Company, News
from user.models import Profile


class NewsSerializer(ModelSerializer):
    """."""

    class Meta:
        model = News
        fields = '__all__'

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    company = serializers.SlugRelatedField(slug_field='name',
                                          read_only=True)

class CompanySerializer(ModelSerializer):
    """."""

    class Meta:
        model = Company
        fields = '__all__'
        # exclude = ('id',)

    # author = serializers.SlugRelatedField(slug_field='username',
    #                                       read_only=True)

    # def validate(self, data):
    #     """У автора только один обзор к Title."""
    #     if self.context['request'].method == 'POST':
    #         title_id = self.context['view'].kwargs['title_id']
    #         author = self.context['request'].user
    #         review_exists = Review.objects.filter(
    #             author=author,
    #             title=title_id).exists()
    #         if review_exists:
    #             code_400 = status.HTTP_400_BAD_REQUEST
    #             raise serializers.ValidationError(code=code_400)
    #     return data


class CompanyDetailSerializer(ModelSerializer):
    """."""

    class Meta:
        model = Company
        fields = '__all__'

    news = NewsSerializer(many=True, read_only=True)
    amount_of_employees = serializers.SerializerMethodField()

    def get_amount_of_employees(self, obj):
        amount = obj.profiles.all().count()
        return amount




class ProfileSerializer(ModelSerializer):
    """."""

    class Meta:
        model = Profile
        fields = '__all__'
