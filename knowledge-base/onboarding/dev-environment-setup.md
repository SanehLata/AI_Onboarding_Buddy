# Development Environment Setup

## Required Tools
Install the following tools. All are available at `software.techcorp.com` or via the links below.

| Tool | Version | Purpose |
|------|---------|---------|
| Git | 2.40+ | Version control |
| Python | 3.11+ | Primary backend language |
| Node.js | 20 LTS | Frontend tooling |
| Docker Desktop | Latest | Container development |
| VS Code or IntelliJ | Latest | IDE |
| Azure CLI | Latest | Cloud resource management |
| Terraform | 1.6+ | Infrastructure as code |
| kubectl | 1.28+ | Kubernetes management |

## Repository Setup
```bash
# Configure Git with your TechCorp identity
git config --global user.name "Your Name"
git config --global user.email "your.name@techcorp.com"

# Clone your team's main repository
git clone https://github.techcorp.com/your-team/main-service.git
cd main-service

# Install dependencies
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the test suite to verify setup
pytest tests/ -v
```

## Docker Setup
```bash
# Verify Docker is running
docker info

# Build and run the local development stack
docker compose up -d

# Verify all services are healthy
docker compose ps
```

## Environment Variables
Copy the team's `.env.example` file and fill in your local values:
```bash
cp .env.example .env
```
Your onboarding buddy will provide the required secrets for local development. Never commit `.env` files to the repository.

## Database Access
Local development uses Docker-managed PostgreSQL. For staging/production database access, request it through the Access Provisioning Guide.

## IDE Configuration
### VS Code
Install recommended extensions from `.vscode/extensions.json` in the repository. Key extensions: Python, Pylint, Docker, GitLens, Prettier.

### IntelliJ
Import the project as a Python project. Configure the Python interpreter to use the virtual environment created above.

## Verification
Run the following to confirm your environment is fully set up:
```bash
# All should pass
python --version          # 3.11+
docker --version          # 24+
git --version             # 2.40+
az version                # Latest
terraform version         # 1.6+
kubectl version --client  # 1.28+
pytest tests/ -v          # All green
```
