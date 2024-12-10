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
from mininet.log import info, setLogLevel
from mn_wifi.sixLoWPAN.link import LoWPAN
from mininet.term import makeTerm

if '-b' in sys.argv:
    from mn_wifi.energy import Energy
if '-a' in sys.argv:
    from containernet.energy import Energy

def docker_cp(source_path, destination_path):
    try:
        command = ["docker", "cp", f"{source_path}", f"{destination_path}"]

        subprocess.run(command, check=True)
        print(f"Arquivo(s) copiado(s) com sucesso: {source_path} -> {destination_path}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando docker cp: {e}")

def topology():
    net = Containernet(iot_module='mac802154_hwsim', ipBase='192.168.210.0/24')

    dimage = 'ramonfontes/bmv2:lowpan-storing'

    info('*** Adding Nodes...\n')
    sensor1 = net.addSensor('sensor1', ip6='fe80::1/64', panid='0xbeef',
                            dodag_root=True, storing_mode=2, voltage=3.7,
                            cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor2 = net.addSensor('sensor2', ip6='fe80::2/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor3 = net.addSensor('sensor3', ip6='fe80::3/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor4 = net.addSensor('sensor4', ip6='fe80::4/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor5 = net.addSensor('sensor5', ip6='fe80::5/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor6 = net.addSensor('sensor6', ip6='fe80::6/64', panid='0xbeef', voltage=3.7,
                            storing_mode=2, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor7 = net.addSensor('sensor7', ip6='fe80::7/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor8 = net.addSensor('sensor8', ip6='fe80::8/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor9 = net.addSensor('sensor9', ip6='fe80::9/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)
    sensor10 = net.addSensor('sensor10', ip6='fe80::10/64', panid='0xbeef', voltage=3.7,
                            storing_mode=1, cls=DockerSensor, dimage=dimage, cpu_shares=10,
                            volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw"],
                            environment={"DISPLAY": ":0"}, privileged=True)

    net.configureWifiNodes()

    info('*** Creating links...\n')
    net.addLink(sensor1, sensor2, cls=LoWPAN)
    net.addLink(sensor1, sensor3, cls=LoWPAN)
    net.addLink(sensor1, sensor6, cls=LoWPAN)
    net.addLink(sensor2, sensor7, cls=LoWPAN)
    net.addLink(sensor6, sensor8, cls=LoWPAN)
    net.addLink(sensor6, sensor9, cls=LoWPAN)
    net.addLink(sensor3, sensor4, cls=LoWPAN)
    net.addLink(sensor4, sensor5, cls=LoWPAN)
    net.addLink(sensor5, sensor10, cls=LoWPAN)

    info('*** Starting network...\n')
    net.build()

    if '-b' in sys.argv or '-a' in sys.argv:
        info("*** Measuring energy consumption...\n")
        Energy(net.sensors)

    if '-r' in sys.argv:
        net.configRPLD(net.sensors)

    if '-b' in sys.argv:
        makeTerm(sensor1, title='ping', cmd="bash -c 'ping -c50 fe80::2%sensor1-pan0;'")

    if '-a' in sys.argv:
        makeTerm(sensor1, title='stress', cmd="bash -c 'sleep 10 && stress --cpu 1;'")
        makeTerm(sensor2, title='stress', cmd="bash -c 'sleep 20 && stress --cpu 1;'")
        makeTerm(sensor3, title='stress', cmd="bash -c 'sleep 30 && stress --cpu 1;'")
        makeTerm(sensor4, title='stress', cmd="bash -c 'sleep 40 && stress --cpu 1;'")

    for t in range(0, 60):
        print(f"\r{t}", end="", flush=True)
        sleep(1)

    for n in range(1, 5):
        container = f"mn.sensor{n}"
        source = f"{container}:/tmp/consumption.log"
        destination = f"./{container[3:]}.log"
        docker_cp(source, destination)

    os.system('pkill -9 -f xterm')

    if '-b' in sys.argv:
        print("energy consumed by sensor1:", sensor1.wintfs[0].consumption, "mW")
        print("energy consumed by sensor2:", sensor2.wintfs[0].consumption, "mW")
        print("energy consumed by sensor7:", sensor7.wintfs[0].consumption, "mW")

    info('*** Stopping network...\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
