pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = "dubithal/weather-app"
        AWS_CREDENTIALS = credentials('aws-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                dir('app') {
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Login to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        
        stage('Push') {
            steps {
                sh "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Deploy to EC2') {
            steps {
                withEnv(["AWS_ACCESS_KEY_ID=${AWS_CREDENTIALS_USR}", "AWS_SECRET_ACCESS_KEY=${AWS_CREDENTIALS_PSW}", "AWS_DEFAULT_REGION=us-east-1"]) {
                    sh '''
                        # Find the instance ID based on the private IP address
                        INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=private-ip-address,Values=3.95.31.133" --query "Reservations[0].Instances[0].InstanceId" --output text)

                        echo "Deploying to EC2 instance with ID: $INSTANCE_ID"

                        # Send remote command via SSM
                        COMMAND_ID=$(aws ssm send-command \
                          --instance-ids $INSTANCE_ID \
                          --document-name "AWS-RunShellScript" \
                          --parameters commands=["cd /home/ec2-user/dubi-proj/app && docker-compose down && docker pull dubithal/weather-app:latest && docker-compose build --no-cache flask nginx && docker-compose up -d"] \
                          --output text --query "Command.CommandId")

                          echo "SSM command ID: $COMMAND_ID"

                          # Wait for the command to complete
                          sleep 5

                          # Check the status of the command
                          aws ssm get-command-invocation \
                            --command-id $COMMAND_ID \
                            --instance-id $INSTANCE_ID \
                            --query "Status"

                    '''
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
