from django.db import models
from django.conf import settings

class SingleTokenModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

class GitHubConfig(SingleTokenModel):
    token = models.CharField(max_length=100, help_text="Default GitHub Access Token")


class Repository(models.Model):
    owner = models.CharField(max_length=100, help_text="GitHub username")
    name = models.CharField(max_length=100, help_text="repo slug")
    token = models.CharField(max_length=100, blank=True, help_text="token is option (it will use default token)")

class PullRequest(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    pr_number = models.IntegerField()
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    