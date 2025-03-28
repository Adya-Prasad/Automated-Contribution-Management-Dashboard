from django.shortcuts import render
from django.db.models import Avg, Count, Max
from django.utils import timezone
from .models import Repository, PullRequest
from django.db import models
from pathlib import Path

def dashboard(request):
    repos = Repository.objects.annotate(
        open_prs=Count('pullrequest', filter=models.Q(pullrequest__status='open')),
        stale_prs=Count('pullrequest', 
                       filter=models.Q(pullrequest__status='open') & 
                       models.Q(pullrequest__age__gte=7))
    )
    
    # Global stats
    global_stats = {
        'total_prs': PullRequest.objects.count(),
        'avg_age': PullRequest.objects.aggregate(avg=Avg('age'))['avg'] or 0,
        'oldest_pr': PullRequest.objects.order_by('-age').first()
    }
    
    # Add per-repo stats
    for repo in repos:
        repo.stats = {
            'open_prs': repo.open_prs,
            'stale_prs': repo.stale_prs,
            'avg_response': PullRequest.objects.filter(repo=repo)
                             .aggregate(avg=Avg('age'))['avg'] or 0
        }
    
    context = {
        'repos': repos,
        'global_stats': global_stats,
        'recent_activity': PullRequest.objects.select_related('repo')
                              .order_by('-updated_at')[:20]
    }
    return render(request, 'dashboard.html', context)

def add_repository(request):
    return render(request, 'add_repo.html', {})

def add_demo_repository(request):
    return render(request, 'add_demo_repo.html', {})

def removal_request(request):
    return render(request, 'removal_request.html', {})

def read_documentation_file(filename):
    docs_dir = Path(__file__).parent.parent / 'docs'
    file_path = docs_dir / filename
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    return None

def documentation_home(request):
    context = {
        'backend_doc': read_documentation_file('backend.html'),
        'security_doc': read_documentation_file('report.html'),
    }
    return render(request, 'documentation.html', context)