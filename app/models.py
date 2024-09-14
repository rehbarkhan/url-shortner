from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.

class URLModel(models.Model):
    _retention = (
        ('1 Week', '1 Week'),
        ('Permanent', 'Permanent')
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    url = models.URLField()
    short_url = models.URLField(null=True, blank=True) # generate backend.
    retention = models.CharField(max_length=20, choices=_retention)

    def save(self, *args, **kwargs):
        flag = True
        while flag:
            short_url = get_random_string(length=5)
            if URLModel.objects.filter(short_url = short_url).exists():
                pass
            else:
                break
        self.short_url = short_url
        return super(URLModel, self).save(*args, **kwargs)

from django import forms

class URLModelForm(forms.ModelForm):
    class Meta:
        model = URLModel
        fields = ['url','retention']




