pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        FLASK_IMAGE = 'dubithal/weather-app:latest'
        NGINX_IMAGE = 'dubithal/nginx:latest'
        AWS_CREDENTIALS = credentials('aws-credentials')
        EC2_INSTANCE_TAG_KEY = "Name"
        EC2_INSTANCE_TAG_VALUE = "weather-app-server"
        AWS_REGION = "us-east-1"
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
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
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
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker push $NGINX_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([[ 
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    credentialsId: 'aws-credentials' 
                ]]) {
                    script {
                        def deployCommand = """
                            cd ~/dubi-proj &&
                            git pull origin main &&
                            cd app &&
                            docker pull dubithal/weather-app:latest &&
                            docker pull dubithal/nginx:latest &&
                            docker compose down &&
                            docker compose up -d
                        """

                        sh """
                            aws ssm send-command \\
                                --region $AWS_REGION \\
                                --document-name "AWS-RunShellScript" \\
                                --comment "Deploy weather app" \\
                                --targets Key=tag:$EC2_INSTANCE_TAG_KEY,Values=$EC2_INSTANCE_TAG_VALUE \\
                                --parameters commands=["${deployCommand.replace('\n', ' ')}"] \\
                                --output text
                        """ 
                    }
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

