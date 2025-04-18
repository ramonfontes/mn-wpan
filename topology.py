#!/usr/bin/python

"""
@author: Ramon dos Reis Fontes
@email: ramon.fontes@ufrn.br
"""

import os
import sys
import subprocess
from time import sleep

from containernet.net import Containernet
from containernet.node import DockerSensor
from containernet.cli import CLI
from containernet.energy import Energy as DockerEnergy

from mininet.log import info, setLogLevel
from mininet.term import makeTerm
from mn_wifi.energy import Energy as WifiEnergy
from mn_wifi.sixLoWPAN.link import LoWPAN


def docker_cp(source_path, destination_path):
    """
    Copy files from a Docker container to a local path.
    """
    try:
        command = ["docker", "cp", source_path, destination_path]
        subprocess.run(command, check=True)
        print(f"File(s) copied: {source_path} -> {destination_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error when running docker cp command: {e}")


def create_sensors(net, dimage):
    """
    Create and return a list of configured sensors.
    """
    sensors = []
    for i in range(1, 11):
        storing_mode = 2 if i in [1, 6] else 1
        is_root = i == 1
        sensor = net.addSensor(
            f'sensor{i}', ip6=f'fe80::{i}/64', panid='0xbeef',
            dodag_root=is_root, storing_mode=storing_mode, voltage=3.7,
            cls=DockerSensor, dimage=dimage, cpu_shares=10,
            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
            environment={"DISPLAY": ":0"}, privileged=True
        )
        sensors.append(sensor)
    return sensors


def create_links(net, sensors):
    """
    Create LoWPAN links between sensors based on a predefined topology.
    """
    links = [
        (0, 1), (0, 2), (0, 5), (1, 6),
        (5, 7), (5, 8), (2, 3), (3, 4), (4, 9)
    ]
    for a, b in links:
        net.addLink(sensors[a], sensors[b], cls=LoWPAN)


def topology():
    """
    Define and configure the IoT network topology using Containernet.
    """
    net = Containernet(ipBase='192.168.210.0/24')
    dimage = 'ramonfontes/bmv2:lowpan-storing'

    info('*** Adding Nodes...\n')
    sensors = create_sensors(net, dimage)

    net.configureWifiNodes()

    info('*** Creating links...\n')
    create_links(net, sensors)

    info('*** Starting network...\n')
    net.build()

    if '-b' in sys.argv:
        WifiEnergy(net.sensors)
    if '-a' in sys.argv:
        DockerEnergy(net.sensors)
    if '-r' in sys.argv:
        net.configRPLD(net.sensors)

    if '-b' in sys.argv:
        makeTerm(sensors[0], title='ping', cmd="bash -c 'ping -c50 fe80::2%sensor1-pan0;'")

    if '-a' in sys.argv:
        for i, delay in enumerate([10, 20, 30, 40]):
            makeTerm(sensors[i], title='stress', cmd=f"bash -c 'sleep {delay} && stress --cpu 1;'")

        for t in range(60):
            print(f"\r{t}", end="", flush=True)
            sleep(1)

        for n in range(1, 5):
            container = f"mn.sensor{n}"
            docker_cp(f"{container}:/tmp/consumption-cpu", f"./sensor{n}.log")

    if '-a' not in sys.argv:
        info('*** Running CLI...\n')
        CLI(net)

    os.system('pkill -9 -f xterm')

    if '-b' in sys.argv:
        for i in [0, 1, 6]:  # sensor1, sensor2, sensor7
            print(f"energy consumed by sensor{i+1}:", sensors[i].wintfs[0].consumption, "Wh")

    info('*** Stopping network...\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
