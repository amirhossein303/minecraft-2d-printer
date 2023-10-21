FROM openjdk:18-slim-bullseye

WORKDIR minecraft-server

RUN mkdir plugins
COPY ./server_templates/eula.txt .
COPY ./server_templates/server.properties .
COPY ./server_templates/server.jar .
COPY ./server_templates/plugins ./plugins

ENTRYPOINT ["java", "-Xms1G", "-Xmx2G", "-jar", "server.jar", "nogui"]