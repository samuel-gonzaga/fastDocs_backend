from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('meeting', "Reunião"),
        ('payment', "Pagamento"),
        ('other', "Outro"),
    ]

    title = models.CharField("Título", max_length=200)
    date = models.DateField("Data")
    time = models.TimeField("Hora", blank=True, null=True)
    category = models.CharField("Categoria", max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField("Descrição", blank=True, null=True)
    password = models.CharField("Senha", max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return f"{self.title} ({self.date})"
