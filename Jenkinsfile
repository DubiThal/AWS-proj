pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('DOCKERHUB_CREDENTIALS_ID')
        DOCKERHUB_USERNAME = 'dubithal'
        FLASK_IMAGE = 'dubithal/weather-app:latest'
        NGINX_IMAGE = 'dubithal/nginx:latest'
        EC2_SSH_KEY = credentials('EC2_SSH_PRIVATE_KEY')
        EC2_USER = 'ec2-user'
        EC2_HOST = 'www.dubiapp.duckdns.org'
    }

    stages {
        stage('Test Flask') {
            steps {
                dir('app') {
                    sh 'python3 -m unittest discover -s tests'
                }
            }
        }

        stage('Lint NGINX Config') {
            steps {
                dir('app') {
                    sh '''
                        docker run --rm -v "$PWD/nginx.conf":/etc/nginx/nginx.conf nginx:latest nginx -t
                    '''
                }
            }
        }

        stage('Build and Push Flask Image') {
            steps {
                dir('app') {
                    sh '''
                        docker build -t $FLASK_IMAGE -f Dockerfile .
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_USERNAME --password-stdin
                        docker push $FLASK_IMAGE
                    '''
                }
            }
        }

        stage('Build and Push NGINX Image') {
            steps {
                dir('app') {
                    sh '''
                        docker build -t $NGINX_IMAGE -f Dockerfile.nginx .
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_USERNAME --password-stdin
                        docker push $NGINX_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['EC2_SSH_PRIVATE_KEY']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            cd ~/dubi-proj &&
                            git pull origin main && 
                            cd app &&
                            docker pull $FLASK_IMAGE &&
                            docker pull $NGINX_IMAGE &&
                            docker compose down &&
                            docker compose up -d
                        '
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}

