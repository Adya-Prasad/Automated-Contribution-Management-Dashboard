from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Repository, PullRequest, GitHubConfig

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'repo', 'pr_number', 'status', 'age')

class RepositoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.token and not GitHubConfig.objects.exists():
            raise ValidationError("Either set a global token or provide repository-specific token")
        super().save_model(request, obj, form, change)
