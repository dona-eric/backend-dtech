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
    Envoie un mail à l'admin + un mail automatique à l'utilisateur (si email existe).
    """
    permission_classes = [permissions.AllowAny]
    email_subject = ""
    email_message_template = ""
    user_confirmation_subject = "Merci pour votre message"
    user_confirmation_template = "Bonjour {name},\n\nNous avons bien reçu votre message et nous vous répondrons très bientôt.\n\nCordialement,\nL'équipe DTech-Africa"
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = request.data

        # Envoi à l’admin
        if getattr(settings, "ADMIN_EMAIL", None):
            send_mail(
                subject=self.email_subject,
                message=self.email_message_template.format(**data),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

        # Réponse automatique à l’utilisateur
        if "email" in data and data["email"]:
            send_mail(
                subject=self.user_confirmation_subject,
                message=self.user_confirmation_template.format(**data),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[data["email"]],
                fail_silently=True,  # ne bloque pas si l’utilisateur a mis un mauvais mail
            )

        return response


class SignupViewSet(NotifyCreateModelViewSet):
    queryset = Signup.objects.all().order_by("-created_at")
    serializer_class = SignupSerializer
    email_subject = "Nouvelle inscription"
    email_message_template = "Nouvelle inscription de {name} ({email})."
    user_confirmation_subject = "Bienvenue chez DTech-Africa 🎉"
    user_confirmation_template = "Bonjour {name},\n\nMerci de vous être inscrit à nos programmes ! Nous vous contacterons bientôt.\n\nL'équipe DTech-Africa"

class ContactViewSet(NotifyCreateModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer
    email_subject = "Nouveau message de contact"
    email_message_template = "De: {name} <{email}>\n\n{message}"
    user_confirmation_subject = "Votre message a bien été reçu"
    user_confirmation_template = "Bonjour {name},\n\nMerci pour votre message. Notre équipe reviendra vers vous dans les plus brefs délais.\n\nL'équipe DTech-Africa"

class NewsletterViewSet(NotifyCreateModelViewSet):
    queryset = Newsletter.objects.all().order_by('-created_at')
    serializer_class = NewsletterSerializer
    email_subject = "Nouvelle inscription à la newsletter"
    email_message_template = "Nouvelle inscription: {email}"
    user_confirmation_subject = "Bienvenue à la newsletter DTech-Africa"
    user_confirmation_template = "Bonjour,\n\nMerci de vous être abonné à notre newsletter ! Vous recevrez bientôt nos actualités.\n\nL'équipe DTech-Africa"



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