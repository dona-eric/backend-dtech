from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Signup, Contact, Newsletter, Articles, Trainer, Training, Project
from rest_framework.pagination import PageNumberPagination
from .serializers import SignupSerializer, ContactSerializer, NewsletterSerializer, ArticleSerializer, TrainerSerializer, TrainingSerializer, ProjectSerializer
from .utils import send_email
from django.conf import settings
from django.core.mail import send_mail
class NotifyCreateModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet générique avec notification email après création.
    """
    permission_classes = [permissions.AllowAny]

    email_subject = ""
    email_message_template = ""
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = request.data
        send_email(
            subject=self.email_subject,
            message=self.email_message_template.format(**data),
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
        return response


class SignupViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all().order_by("-created_at")
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        signup = serializer.save()
        # Email admin (optionnel)
        if getattr(settings, "DEFAULT_FROM_EMAIL", None):
            send_mail(
                subject="Nouvelle inscription",
                message=f"Nouvelle inscription de {signup.name} ({signup.email}).",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )

class ContactViewSet(NotifyCreateModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save()
        if getattr(settings, "DEFAULT_FROM_EMAIL", None):
            send_mail(
                subject="Nouveau message de contact",
                message=f"De: {contact.name} <{contact.email}>\n\n{contact.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
class NewsletterViewSet(NotifyCreateModelViewSet):
    queryset = Newsletter.objects.all().order_by('-created_at')
    serializer_class = NewsletterSerializer
    email_subject = "Nouvelle inscription à la newsletter"
    email_message_template = "Nouvelle inscription: {email}"


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('trainings__trainer').all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all().order_by('-created_at')
    serializer_class = TrainerSerializer
    permission_classes = [permissions.AllowAny]

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all().order_by('-created_at')
    serializer_class = TrainingSerializer
    permission_classes = [permissions.AllowAny]