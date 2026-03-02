from django.db import models
from forums.models import Author, User
from  django.utils import timezone
# Create your models here.

class OneTimeCode(models.Model):
    code = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # или ForeignKey, но обычно один код на пользователя, так что OneToOne
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        # например, код действителен 10 минут
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() < 600