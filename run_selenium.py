import logging
import docker

logging.basicConfig(format="%(message)s", level=logging.INFO)

client = docker.from_env()

network = client.networks.create("grid", driver="bridge")
logging.info("Created network %s %s", network.name, network.id)

hub_container = client.containers.run(
    "selenium/hub:4.0.0-beta-1-prerelease-20210204",
    command=None,
    detach=True,
    auto_remove=True,
    stderr=True,
    ports={4442: 4442, 4443: 4443, 4444: 4444},
    network="grid",
    name="selenium-hub",
)
logging.info("Created container %s %s", hub_container.name, hub_container.id)

chrome_container = client.containers.run(
    "selenium/node-chrome:4.0.0-beta-1-prerelease-20210204",
    command=None,
    detach=True,
    auto_remove=True,
    stderr=True,
    environment=[
        "SE_EVENT_BUS_HOST=selenium-hub",
        "SE_EVENT_BUS_PUBLISH_PORT=4442",
        "SE_EVENT_BUS_SUBSCRIBE_PORT=4443",
    ],
    volumes={"/dev/shm": {"bind": "/dev/shm", "mode": "rw"}},
    network="grid",
    name="node-chrome",
)
logging.info("Created container %s %s", chrome_container.name, chrome_container.id)


# $ docker network create grid
# $ docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:4.0.0-beta-1-prerelease-20210204
# $ docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
#     -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
#     -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
#     -v /dev/shm:/dev/shm \
#     selenium/node-chrome:4.0.0-beta-1-prerelease-20210204
