from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout

try:
    from bson import ObjectId
except Exception:
    ObjectId = None


class SafeModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if ObjectId is None:
            return rep

        def _convert(value):
            if isinstance(value, ObjectId):
                return str(value)
            if isinstance(value, dict):
                return {k: _convert(v) for k, v in value.items()}
            if isinstance(value, list):
                return [_convert(v) for v in value]
            return value

        return _convert(rep)


class UserSerializer(SafeModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeamSerializer(SafeModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ActivitySerializer(SafeModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class LeaderboardSerializer(SafeModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'


class WorkoutSerializer(SafeModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
