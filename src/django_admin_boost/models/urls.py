from django.db import models

class UrlModel(models.Model):
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"