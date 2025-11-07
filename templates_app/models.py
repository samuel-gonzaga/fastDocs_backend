from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file = models.FileField()
    file_content = models.BinaryField(null=True, blank=False)
    placeholders = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Lista de placeholders do template"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de criação"
    )

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ["-created_at"]


    def __str__(self):
        return self.name