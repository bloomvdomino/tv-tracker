from rest_framework import serializers

from .models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    show_status_text = serializers.SerializerMethodField()

    class Meta:
        model = Progress
        fields = ('user', 'show_id', 'show_name', 'show_poster_path', 'show_status', 'show_status_text',
                  'current_season', 'current_episode', 'next_season', 'next_episode', 'next_air_date',
                  'updated', 'is_followed', 'is_scheduled', 'is_available', 'is_finished')

    def get_show_status_text(self, obj):
        return obj.get_show_status_display()
