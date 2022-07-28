from django.db import models


class TeamMember(models.Model):
    firstName = models.CharField(max_length=200, null=True, blank=True)
    lastName = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12, null=True, blank=True)
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.firstName + self.lastName

    class Meta:
        ordering = ['created']
