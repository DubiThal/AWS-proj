FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/nginx/ssl

COPY server.crt /etc/nginx/ssl/
COPY server.key /etc/nginx/ssl/

RUN mkdir -p /etc/nginx/conf.d
COPY nginx.conf /etc/nginx/conf.d/jenkins.conf

EXPOSE 23230 23443

RUN echo '#!/bin/bash\n\
service nginx start\n\
exec /usr/local/bin/jenkins.sh' > /usr/local/bin/start.sh && \
chmod +x /usr/local/bin/start.sh

USER jenkins

ENV JENKINS_OPTS="--httpPort=8080"
ENV JENKINS_SLAVE_AGENT_PORT=50000

ENTRYPOINT ["/usr/local/bin/start.sh"]
