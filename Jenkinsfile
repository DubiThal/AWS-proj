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
        WEATHER_API_KEY = '' 
    }

    stages {
        stage('Get Secrets from SSM') {
          steps {
            script {
              def apiKey = sh(
                script: "aws ssm get-parameter --name \"weather_api_key\" --with-decryption --region us-east-1 --query 'Parameter.Value' --output text",
                returnStdout: true
              ).trim()

              env.WEATHER_API_KEY = apiKey
            }
          }
        }

        stage('Test Flask') {
            steps {
                dir('app') {
                   sh """
                       export WEATHER_API_KEY="${WEATHER_API_KEY}"
                       PYTHONPATH=$(pwd) python3 -m pytest tests
                   """
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
                            export HOME=/home/ec2-user &&
                            cd /home/ec2-user/dubi-proj &&
                            git remote set-url origin https://github.com/dubithal/dubi-proj.git &&
                            git pull origin main &&
                            cd app &&
                            docker pull dubithal/weather-app:latest &&
                            docker pull dubithal/nginx:latest &&
                            echo WEATHER_API_KEY="${WEATHER_API_KEY}" > .env &&
                            docker-compose down &&
                            docker-compose up -d
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
            script {
                env.WEATHER_API_KEY = ''
            }
        }
    }
}

