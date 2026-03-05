from rest_framework import serializers
from .models import (
    Subject,
    UserSubject,
    Streak,
    Topic,
    StudyMaterial,
    Roadmap,
    RoadmapDay,
    RoadmapTask,
    Assignment,     
    Question,
    Choice,
    AbilityScore,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class UserSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubject
        fields = '__all__'


class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class AbilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityScore
        fields = '__all__'
        
class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = '__all__'

class RoadmapDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapDay
        fields = '__all__'

class RoadmapTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapTask
        fields = '__all__'