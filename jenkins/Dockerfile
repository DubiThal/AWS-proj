FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y \
    git \
    docker.io \
    curl \
    sudo \
    openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN jenkins-plugin-cli --plugins \
    git \
    pipeline-stage-view \
    docker-workflow \
    github \
    credentials \
    workflow-aggregator \
    blueocean \
    configuration-as-code\
    github-branch-source \
    git-client \
    git-server \
    multibranch-scan-webhook-trigger

RUN usermod -aG docker jenkins

USER jenkins

ENV JENKINS_OPTS="--httpPort=8080"
ENV JENKINS_SLAVE_AGENT_PORT=50000

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

