from django.utils import timezone
from github import Github
from github.GithubException import GithubException
from automated_contribution_management.models import Repository, PullRequest, GitHubConfig

def run(*args, **kwargs):
    if not GitHubConfig.objects.exists():
        print("⛔ Critical Error: No global GitHub token configured!")
        print("   Go to /admin to add token in GitHub Config")
        return
    
    # Rest of run() code

def update_prs():
    repos = Repository.objects.all()
    if not repos.exists():
        print("⚠️ No repositories configured in admin")
        return
    
    try:
        github_config = GitHubConfig.objects.first()
        global_token = github_config.token if github_config else None
    except GitHubConfig.DoesNotExist:
        global_token = None

    for repo in repos:
        print(f"\nProcessing repository: {repo.owner}/{repo.name}")
        try:

            # Use repo-specific token or fallback to global
            token = repo.token or global_token
            if not token:
                raise ValueError(f"No token found for {repo.owner}/{repo.name}")
            
            g = Github(repo.token)
            repo_obj = g.get_repo(f"{repo.owner}/{repo.name}")
            pulls = repo_obj.get_pulls(state='open').get_page(0)
            
            pr_count = 0
            for pr in pulls:
                # Debug output for each PR
                print(f"Processing PR #{pr.number}: {pr.title}")
                
                PullRequest.objects.update_or_create(
                    pr_number=pr.number,
                    repo=repo,
                    defaults={
                        'title': pr.title,
                        'created_at': pr.created_at,
                        'updated_at': pr.updated_at,
                        'status': pr.state,
                        'age': (timezone.now() - pr.created_at).days
                    }
                )
                pr_count += 1
            
            print(f"✅ Successfully processed {pr_count} PRs")
            
        except ValueError as ve:
            print(f"🔴 Configuration Error: {str(ve)}")
            print("   Add token in Admin → GitHub Config or per-repository")
        except GithubException as ge:
            print(f"🔴 GitHub Error ({ge.status}): {ge.data.get('message', 'Unknown error')}")
            if ge.status == 404:
                print(f"Verify repository exists: https://github.com/{repo.owner}/{repo.name}")
        except Exception as e:
            print(f"🔴 Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()

def managing_aging_queue(repo):
    stale_prs = PullRequest.objects.filter(
        repo = repo,
        status = 'open',
        age__get=7
    )

    for pr in stale_prs:
        # Auto comment on stale PRs
        github_pr = repo.github_repo.get_pull(pr.pr_number)
        github_pr.create_comment(
             f"⚠️ This PR has been open for {pr.age} days. "
            "Please update its status or it may be closed automatically."
        )

        # Escalate after 14 days
        if pr.age >= 14:
            github_pr.edit(state='closed')
            pr.status = 'closed'
            pr.save()