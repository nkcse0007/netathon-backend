from rest_framework import serializers
from myapps.event.models import CategoryModel, EventModel, EventRegistrationModel
from myapps.authentication.models import OrganizationModel, ArtistModel, UserLoginInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginInfo
        fields = ('name', 'profile_summary')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = ('__all__')

class ArtistSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()
    artist_profile_summary = serializers.SerializerMethodField()

    class Meta:
        model = ArtistModel
        fields = ('artist_name', 'artist_profile_summary')

    def get_artist_name(self, instance):
        return instance.user.name

    def get_artist_profile_summary(self, instance):
        return instance.user.profile_summary

class EventSearchValidationSerializer(serializers.Serializer):
    SORT_CHOICES = (
        ('asc', 'asc'),
        ('dec', 'dec'),
    )
    FILTER_TYPE_CHOICES = (
        ('upcoming', 'upcoming'),
        ('recomend', 'recomend'),
    )
    query = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city=serializers.CharField(required=False)
    category = serializers.ListField(required=False)
    limit = serializers.IntegerField(default=10, required=False)
    order_by = serializers.CharField(required=False)
    filter_type = serializers.ChoiceField(choices=FILTER_TYPE_CHOICES, required=False)
    sort = serializers.ChoiceField(choices=SORT_CHOICES, required=False)


class EventSearchSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source="organization.name")
    organizer_intro = serializers.CharField(source="organization.profile_summary")
    artists = ArtistSerializer(read_only=True, many=True)

    class Meta:
        model = EventModel
        fields = (
            'id', 'organizer_name', 'organizer_intro', 'artists', 'title', 'intro', 'grid_image', 'banner', 'city', 'location', 'regular_price', 
            'sale_price', 'event_date', 'created_at'
        )
