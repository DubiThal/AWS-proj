# 🌤️ Weather Forecast App – DevOps Project by Dubi Thal

## 🎯 Overview
Flask-based weather forecast web application deployed in a Docker container on an AWS EC2 instance. The project uses Jenkins for CI/CD, Terraform for infrastructure management and includes Prometheus and Grafana for monitoring and visualization. GitHub and DockerHub are integrated for version control and image storage.  
**Weather data is retrieved via the [OpenWeatherMap API](https://openweathermap.org/api).**

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
| Prometheus  | Monitoring                      |
| Grafana     | Visualization                   |

## 🧱 Infrastructure Setup
- **Cloud Provider**: AWS
- **Provisioning Tool**: Terraform

**Resources Created**:
- VPC
- Subnet
- Internet Gateway
- Security Group
- EC2 Instance (Amazon Linux 2) – used to run Jenkins, Flask app, NGINX, Prometheus and Grafana as containers

## 🐳 Docker Setup
The project contains 3 Docker Compose setups:

- **flask & NGINX** – Contains the Flask application and NGINX reverse proxy.
- **jenkins** – Contains the Jenkins server, fully Dockerized with a customized Dockerfile and pre-installed plugin.
- **prometheus & grafana** – Contains configuration files and services for monitoring.

NGINX serves as a secure reverse proxy for the Flask app (port 443) and handles HTTPS via Let's Encrypt certificates.

## 🔁 CI/CD Pipeline (Jenkins)
The Jenkins pipeline performs the following:
- Retrieves Secrets from SSM
- Runs Flask unit tests using pytest 
- Builds the Docker image for the Flask app and NGINX
- Pushes the images to DockerHub
- Deploy to EC2: pulling repository from github, pulls the latest images from DockerHub and reinstalling the containers

## 🔒 Security
- HTTPS enabled via Let's Encrypt certificates
- Secrets are not stored in code – retrieved from AWS SSM
- Docker containers run as non-root users where applicable
- AWS, GitHub, and DockerHub credentials are securely stored and managed within Jenkins Credentials Store, and used in the CI/CD pipeline to authenticate and interact with respective services securely.
- No secrets or sensitive information are hardcoded in the repository or Docker images.
