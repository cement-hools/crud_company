from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Company, News
from user.models import Profile, User


class NewsSerializer(ModelSerializer):
    """Сериалайзер новостей."""

    class Meta:
        model = News
        fields = '__all__'

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    company = serializers.SlugRelatedField(slug_field='name',
                                           read_only=True)


class CompanySerializer(ModelSerializer):
    """Сериалайзер компаний."""

    class Meta:
        model = Company
        fields = '__all__'


class CompanyDetailSerializer(ModelSerializer):
    """Сериалайзер подробной информации о компании."""

    class Meta:
        model = Company
        fields = '__all__'

    news = NewsSerializer(many=True, read_only=True)
    amount_of_employees = serializers.SerializerMethodField()

    def get_amount_of_employees(self, obj):
        amount = obj.profiles.all().count()
        return amount


class ProfileSerializer(ModelSerializer):
    """Сериалайзер профилей."""

    class Meta:
        model = Profile
        fields = '__all__'

    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=User.objects.all())
