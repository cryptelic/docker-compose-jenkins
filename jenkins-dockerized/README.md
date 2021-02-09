# Socket solution to run Docker from Jenkins, while Jenkins itself is in a container

This looks like Docker-in-Docker, feels like Docker-in-Docker, but it’s not Docker-in-Docker...

[Read the blog post of DinD feature author](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci).

Multiple different projects require different environments. Because of that, it makes sense to run all tasks in separate dockers. Given solution makes possible to run a docker with a host daemon instead of a container inside the container. With that, proper permissions for docker.sock should be granted.

## Add jenkins user to the docker user's group and restart docker

    usermod -aG docker jenkins
    sudo service docker restart

## Check jenkins user uid on host and set it to HOST_UID

    id -u jenkins

## Check gid for docker group on host and et it to HOST_GID

    getent group | grep docker

## Give permissions for Jenkins files

    sudo chgrp -R jenkins /data/jenkins
    sudo chown -R jenkins /data/jenkins

## Run

    docker-compose up -d

With this configuration, you can run Jenkins in docker and use docker for builds.
