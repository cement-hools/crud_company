from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Company


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
