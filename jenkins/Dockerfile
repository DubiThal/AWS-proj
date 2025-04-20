FROM jenkins/jenkins:lts

USER root

USER jenkins

ENV JENKINS_OPTS="--httpPort=8080"
ENV JENKINS_SLAVE_AGENT_PORT=50000

ENTRYPOINT ["python", "app.py"]

