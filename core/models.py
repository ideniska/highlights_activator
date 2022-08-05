from django.db import models
from django.conf import settings

class UserFiles(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)
    file = models.FileField(upload_to='user_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

