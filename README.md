# 🌤️ Weather Forecast App – DevOps Project

## 🎯 Overview
This is a Flask-based weather forecast web application deployed in a Docker container on an AWS EC2 instance. The project uses Jenkins for CI/CD and Terraform for infrastructure management. GitHub and DockerHub are integrated for version control and image storage.

## 🧱 Infrastructure Setup
- **Cloud Provider**: AWS (Free Tier)
- **Provisioning Tool**: Terraform

**Resources Created**:
- VPC
- Subnet
- Internet Gateway
- Security Group
- EC2 Instance (Amazon Linux 2) – named "jenkins" but used to run both Jenkins and the Flask app

## ⚙️ Tools & Technologies
| Tool        | Purpose                         |
|-------------|----------------------------------|
| Flask       | Web framework for Python        |
| Docker      | Containerization                |
| Jenkins     | CI/CD server (running in Docker)|
| Git         | Version control                 |
| GitHub      | Source code hosting             |
| DockerHub   | Image repository                |
| Terraform   | Infrastructure-as-Code          |
| NGINX       | Reverse proxy and HTTPS support |

## 🐳 Docker Setup
The project contains two Docker Compose setups:

- **app/** – Contains the Flask application and NGINX reverse proxy.
- **jenkins/** – Contains the Jenkins server, fully Dockerized with customized Dockerfile and plugins.

Jenkins is configured via Docker Compose and listens on port 8080.
NGINX serves as a secure reverse proxy for the Flask app (port 443).

## 🔁 CI/CD Pipeline (Jenkins)
The Jenkins pipeline (defined in `Jenkinsfile`) performs the following:
- Clones the GitHub repository
- Builds the Docker image for the Flask app
- Pushes the image to DockerHub
- *(Future)* Deploys to Kubernetes (currently disabled)

## 🧪 Future Enhancements
- ✅ Add HTTPS via Let's Encrypt and NGINX *(in progress)*
- ✅ Split NGINX and Jenkins into separate docker-compose files *(done)*
- 🔜 Run automated tests (e.g., Pytest)
- 🔜 Integrate Prometheus & Grafana for monitoring
- 🔜 Use a lightweight K8s solution like K3s
- 🔜 Store configuration/secrets with AWS SSM or Secrets Manager
