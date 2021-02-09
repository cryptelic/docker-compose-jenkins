import os
import logging
import docker

logging.basicConfig(format="%(message)s", level=logging.INFO)

client = docker.from_env()
TAG = "cryptelic/troposphere:2.6.3"

logging.info("Building docker image %s", TAG)
image, build_logs = client.images.build(
    path="./troposphere-dockerized", tag=TAG, forcerm=True
)

for chunk in build_logs:
    if "stream" in chunk:
        for line in chunk["stream"].splitlines():
            logging.debug(line)

logging.info("Built successfully %s", image.id)

path = os.path.abspath("troposphere-dockerized/example")

container = client.containers.run(
    TAG,
    auto_remove=True,
    stderr=True,
    command=["fab", "-l"],
    volumes={path: {"bind": "/troposphere", "mode": "ro"}},
)

logging.info(container.decode())

# $ docker build -t cryptelic/troposphere:2.6.3 $PWD/troposphere-dockerized
# $ docker run -v $PWD/troposphere-dockerized/example:/troposphere \
#   -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION \
#   cryptelic/troposphere:2.6.3 fab list_stacks
