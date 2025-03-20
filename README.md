# Automated Contribution Management Dashboard

Hello, hello, It's ADYA and...

It is a Django-based dashboard for managing and automating GitHub repository contributions and pull request workflows.

Check out this project here: [https://adyaprasad.pythonanywhere.com/](https://adyaprasad.pythonanywhere.com/)

Read the docs here: [https://adyaprasad.pythonanywhere.com/documentation/](https://adyaprasad.pythonanywhere.com/documentation/)

## 🎯 Features

- **Real-time Repository Monitoring**: Track multiple GitHub repositories
- **Pull Request Management**: Automated tracking of PR status, age, and activity
- **Stale PR Detection**: Identifies and manages inactive pull requests
- **Global & Per-Repository Analytics**: 
  - Total repositories and open PRs
  - Average PR age
  - Response time metrics
  - Stale PR counts
- **Automated Workflows**:
  - Auto-commenting on stale PRs
  - Automatic PR closure after prolonged inactivity
  - Periodic status updates

## 🛠️ Tech Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite3
- **GitHub Integration**: PyGithub 2.6.1
- **Authentication**: Django Admin
- **Task Automation**: Django Extensions
- **CI/CD**: Jenkins, GitHub Actions

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- Git

### Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/automated-contribution-management.git
cd automated-contribution-management
```

2. Create and activate virtual environment:
```sh
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Configure environment variables:
```sh
cp .env.example .env.production
```
Edit `.env.production` with your configuration:
```
DJANGO_SECRET_KEY=your_secret_key
GITHUB_TOKEN=your_github_token
```

5. Run migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```sh
python manage.py createsuperuser
```

7. Start development server:
```sh
python manage.py runserver
```

## 🔧 Configuration

### GitHub Token Setup

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate a new token with required permissions:
   - `repo` access
   - `read:org`
3. Add token in Django admin under GitHub Config

### Repository Management

1. Access Django admin panel at `/admin`
2. Add repositories under Repository model
3. Optional: Configure per-repository tokens

## 🤖 Automation

### PR Management Script

The system runs automated checks every 30 minutes to:
- Update PR statuses
- Detect stale PRs
- Add reminder comments
- Close inactive PRs

### CI/CD Integration

- **Jenkins**: Configured for periodic PR management
- **GitHub Actions**: Automated workflow for PR tracking

## 📊 Dashboard Features

- Global repository statistics
- Per-repository metrics
- Recent activity feed
- Stale PR notifications
- Repository workflow status

## 🔒 Security Notes

- Store sensitive tokens in environment variables
- Use repository-specific tokens when possible
- Regular token rotation recommended
- Keep Django `SECRET_KEY` secure

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📝 License

[Your License] - See LICENSE file for details

## 👨‍💻 Author

Adya Prasad

---
*For Django GSoC 2025*
