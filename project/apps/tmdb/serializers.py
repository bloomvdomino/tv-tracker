from rest_framework import serializers

from .models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Progress
        fields = ('user', 'show_id', 'show_name', 'show_poster_path', 'current_season',
                  'current_episode', 'next_season', 'next_episode', 'next_air_date')
