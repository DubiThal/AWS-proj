🌤️ Weather Forecast App – DevOps Project  
🎯 Overview  
This is a Flask-based weather forecast web application deployed in a Docker container on an AWS EC2 instance. The project uses Jenkins for CI/CD and Terraform for infrastructure management. GitHub and DockerHub are integrated for version control and image storage.  

🧱 Infrastructure Setup
Cloud Provider: AWS (Free Tier)

Provisioning Tool: Terraform

Resources Created:

VPC

Subnet

Internet Gateway

Security Group

EC2 Instance (Amazon Linux 2) – named "jenkins" but used for both Jenkins and the Flask app  

⚙️ Tools & Technologies  

Tool	Purpose  
Flask	Web framework for Python  
Docker	Containerization  
Jenkins	CI/CD server (running in container)  
Git	Version control  
GitHub	Source code hosting  
DockerHub	Image repository  
Terraform	Infrastructure-as-Code  

🐳 Docker Setup  
The project contains two Dockerized components:  

app/ – Flask app with its own Dockerfile  

jenkins/ – Jenkins server with customized Dockerfile and plugins  

Jenkins is configured via Docker Compose and listens on port 8080.  

📂 Project Structure  
.  
├── app/  
│   ├── app.py  
│   ├── Dockerfile  
│   ├── requirements.txt  
│   └── ...  
├── jenkins/  
│   ├── Dockerfile  
│   ├── docker-compose.yml  
│   └── Jenkinsfile  
├── terraform/  
│   ├── main.tf  
│   └── ...  
├── k8s/ (optional for future use)  
└── README.md  

🔁 CI/CD Pipeline (Jenkins)  
The Jenkins pipeline (in jenkins/Jenkinsfile) does the following:  

Clone the repository  

Build the Docker image for the Flask app  

Push the image to DockerHub  

(Future) Deploy to K8s (currently disabled)  

🧪 Future Enhancements  
Add HTTPS (via Let's Encrypt and Nginx)  

Run automated tests (Pytest)  

Integrate Prometheus & Grafana for monitoring  

Use a lightweight K8s solution like K3s  

Store configuration/secrets with AWS SSM or Secrets Manager  
