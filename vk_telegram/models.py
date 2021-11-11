from django.db import models


class MessageOnWall(models.Model):
    type = models.CharField(max_length=255)
    object = models.TextField()
    message = models.TextField(null=True, blank=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    group_id = models.IntegerField()
    message_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись на стене"
        verbose_name_plural = "Записи на стене"

    def __str__(self):
        return f"{self.type} {self.user_name}"
