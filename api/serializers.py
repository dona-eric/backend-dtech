from rest_framework import serializers
from .models import Signup, Contact, Newsletter, Articles, Trainer, Training, Project
from rest_framework.fields import DateTimeField


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'

    def validate_email(self, value):
        if Signup.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà inscrit.")
        return value



class ArticleSerializer(serializers.ModelSerializer):
    created_at = DateTimeField(format="%d/%m/%Y %H:%M")
    class Meta:
        model = Articles
        fields = ['id', 'title', 'excerpt', 'content', 'image', 'created_at']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):
    trainings = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(read_only=True)
    class Meta:
        model = Training
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    trainings = TrainingSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
