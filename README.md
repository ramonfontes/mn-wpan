  # Mininet-WPAN: Enabling WPAN and IoT Emulations with IEEE 802.15.4 Support

Mininet-WPAN leverages the strengths of the Mininet-WiFi architecture by extending it to support wireless personal area networks (WPANs), specifically focusing on the IEEE 802.15.4 protocol. It stands out from the tools mentioned above in several ways:

- Real-time Emulation: It operates as an emulator, allowing real-time experimentation and interaction with actual network configurations. This provides a more realistic environment for testing;
- SDN Integration: built on top of Mininet, Mininet-WPAN inherits strong support for SDN. This enables users to experiment with software-defined networking technologies in low-power networks;
- Lightweight Virtualization: It supports lightweight virtualization, making it scalable and efficient for testing large networks without the overhead of full virtual machine simulations. This makes it particularly suitable for rapid experimentation, debugging, and prototyping;
- Customization and Flexibility: the use of the mac802154 Linux wireless device driver allows Mininet-WPAN to support flexible, low-level manipulation of network interfaces. It is ideal for researchers who need fine-grained control over network behaviors.

## Readme structure

This repository is structured as follows:
```
├── figures  
│   ├── image1.png
│   ├── image2.png
│   ├── image3.png  
├── graph.py 
├── topology.py  
├── LICENSE.md  
└── README.md
```

## Ribbons considered

The ribbons considered are "Artefatos Disponíveis (SeloD)", "Artefatos Funcionais (SeloF)", "Artefatos Sustentáveis (SeloS)", and "Experimentos Reprodutíveis (SeloR)".

## Basic information

- You need to install VirtualBox (tested with version 7.1.6) and load the [Pre-configured Virtual Machine](https://drive.google.com/file/d/1R8n4thPwV2krFa6WNP0Eh05ZHZEdhw4W/view?usp=sharing).
- [topology.py](https://github.com/ramonfontes/mn-wpan/blob/main/topology.py) is the only file that must be run. It contains the virtual nodes and all the necessary configuration.
- [graphy.py](https://github.com/ramonfontes/mn-wpan/blob/main/graph.py) is responsible for running the graph.
- [figures](https://github.com/ramonfontes/mn-wpan/tree/main/figures) folder contains the figures presented within this readme file.

## Dependencies

The pre-configured VM comes with all necessary dependencies pre-installed.

## Security Concerns

The execution of this artifact poses no risk to evaluators.

## Installation

To access the pre-configured VM, use the following credentials: 
- Username: wifi
- Password: wifi

Then, follow these steps:
  - Start the Pre-configured Virtual Machine
  - Open a terminal and clone this repository: `git clone https://github.com/ramonfontes/mn-wpan`
  - Download the Docker Image: `sudo docker pull ramonfontes/bmv2:lowpan-storing`
  - Navigate to the `mn-wpan` directory and follow the steps below.

# Minimal Test 

For a minimum test of Mininet-WPAN operation, we will partially run the Use Case #1.

- Step 1: Running the network topology:  
```
$ sudo python topology.py
```

- Step 2: Pinging `sensor2` to `sensor7`:
```
> sensor2 ping -c1 fe80::7%sensor2-pan0
PING fe80::7%sensor2-pan0(fe80::7%sensor2-pan0) 56 data bytes
64 bytes from fe80::7%sensor2-pan0: icmp_seq=1 ttl=64 time=0.143 ms

--- fe80::7%sensor2-pan0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.143/0.143/0.143/0.000 ms
```
As we can observe, `sensor2` is able to ping `sensor7`, which indicates that nodes within the same communication range or those directly connected through the network topology can interact with each other.

Close Mininet-WPAN with the `exit` command.

## Experiments

Three use cases showcases the capabilities of Mininet-WPAN: a scenario without RPL; other utilizing RPL and the last one about energy consumption. In these case studies, ten IEEE 802.15.4-based wireless sensors were emulated.

### Use Case #1 - Without the Routing Protocol

The network topology:
![](https://raw.githubusercontent.com/ramonfontes/mn-wpan/refs/heads/main/figures/image2.png)

Without a routing protocol, nodes are limited to knowledge of the Link-Local addresses of neighboring sensors. This means they lack routing information for reaching nodes that are more than one hop away, making it impossible to determine the appropriate next hop for multi-hop communication. Consequently, the network lacks a structure for route discovery, and each node only interacts directly with its immediate neighbors without a way to relay data over longer distances.
 
Running the network topology:  
```
$ sudo python topology.py
```

Getting some information of the network interfaces from `sensor1` 
```
> sensor1 ifconfig
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

sensor1-pan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1280
        inet6 fe80::1  prefixlen 64  scopeid 0x20<link>
        unspec AE-A1-14-AC-BD-1F-8A-B9-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 16  bytes 1072 (1.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13  bytes 952 (952.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

sensor1-wpan0: flags=195<UP,BROADCAST,RUNNING,NOARP>  mtu 123
        unspec AE-A1-14-AC-BD-1F-8A-B9-00-00-00-00-00-00-00-00  txqueuelen 300  (UNSPEC)
        RX packets 23  bytes 986 (986.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 14  bytes 784 (784.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Printing the routing table of `sensor1`:
```
> sensor1 route -6 -n
Kernel IPv6 routing table
Destination                    Next Hop                   Flag Met Ref Use If
fe80::/64                      ::                         U    256 3     0 sensor1-pan0
::/0                           ::                         !n   -1  1     0 lo
::1/128                        ::                         Un   0   2     0 lo
fe80::1/128                    ::                         Un   0   5     0 sensor1-pan0
ff00::/8                       ::                         U    256 5     0 sensor1-pan0
::/0                           ::                         !n   -1  1     0 lo
```

Getting IPv6 from `sensor1`:
```
> sensor1 ip -6 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: sensor1-pan0@sensor1-wpan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1280 state UNKNOWN qlen 1000
    inet6 fe80::1/64 scope link 
       valid_lft forever preferred_lft forever
```
  
Getting IPv6 from `sensor2`:
```
> sensor2 ip -6 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: sensor2-pan0@sensor2-wpan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1280 state UNKNOWN qlen 1000
    inet6 fe80::2/64 scope link 
       valid_lft forever preferred_lft forever
```

Getting IPv6 from `sensor7`:
```
> sensor7 ip -6 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: sensor7-pan0@sensor7-wpan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1280 state UNKNOWN qlen 1000
    inet6 fe80::7/64 scope link 
       valid_lft forever preferred_lft forever
```

Pinging from `sensor1` to `sensor2`:
```
> sensor1 ping6 -c1 fe80::2%sensor1-pan0
PING fe80::2%sensor1-pan0(fe80::2%sensor1-pan0) 56 data bytes
64 bytes from fe80::2%sensor1-pan0: icmp_seq=1 ttl=64 time=0.099 ms

--- fe80::2%sensor1-pan0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.099/0.099/0.099/0.000 ms
```

As we can observe, `sensor1` can ping `sensor2`.

Pinging from `sensor1` to `sensor7`:
```
> sensor1 ping -c1 fe80::7%sensor1-pan0
PING fe80::7%sensor1-pan0(fe80::7%sensor1-pan0) 56 data bytes
^C
--- fe80::7%sensor1-pan0 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```
As we can observe, `sensor1` cannot ping `sensor7`.


Pinging `sensor2` to `sensor7`:
```
> sensor2 ping -c1 fe80::7%sensor2-pan0
PING fe80::7%sensor2-pan0(fe80::7%sensor2-pan0) 56 data bytes
64 bytes from fe80::7%sensor2-pan0: icmp_seq=1 ttl=64 time=0.143 ms

--- fe80::7%sensor2-pan0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.143/0.143/0.143/0.000 ms
```
As we can observe, `sensor2` is able to ping `sensor7`, which indicates that nodes within the same communication range or those directly connected through the network topology can interact with each other. This demonstrates a key principle in network communication: only nodes that are directly connected can communicate with each other. This rule is fundamental to understanding how routing protocols, like RPL (Routing Protocol for Low-Power and Lossy Networks), work to establish routes between nodes in a larger network by leveraging intermediate nodes to relay messages between distant devices.

Close Mininet-WPAN with the `exit` command.

### Use Case #2 - With the Routing Protocol

The network topology:
![](https://raw.githubusercontent.com/ramonfontes/mn-wpan/refs/heads/main/figures/image1.png)

When the network operates with the RPL protocol in storage mode there are implications for the scope of IPv6 addresses. In this mode, parent nodes retain and manage the Unique Local Addresses (ULAs) of their child sensors. ULAs are IPv6 addresses that are restricted to a specific network segment or context, meaning they are valid only within a local network and are not routable beyond it.

Running the network topology:  
```
$ sudo python topology.py -r
```

Openning terminals for `sensor1`, `sensor2` and `sensor3`.
```
> xterm sensor1 sensor2 sensor3
```

Getting ip address from `sensor2`:
```
root@sensor2:/# ip -6 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: sensor2-pan0@sensor2-wpan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1280 state UNKNOWN qlen 1000
    inet6 fd3c:be8a:173f:8e80:419:c082:e8cc:26a0/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::2/64 scope link 
       valid_lft forever preferred_lft forever
```

Getting ip address from `sensor7`:
```
root@sensor7:/# ip -6 a 
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: sensor7-pan0@sensor7-wpan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1280 state UNKNOWN qlen 1000
    inet6 fd3c:be8a:173f:8e80:3083:6218:aee4:e62d/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::7/64 scope link 
       valid_lft forever preferred_lft forever
```

Pinging `sensor1` to `sensor2`:
```
root@sensor1:/# ping -c 1 fd3c:be8a:173f:8e80:419:c082:e8cc:26a0
PING fd3c:be8a:173f:8e80:419:c082:e8cc:26a0(fd3c:be8a:173f:8e80:419:c082:e8cc:26a0) 56 data bytes
64 bytes from fd3c:be8a:173f:8e80:419:c082:e8cc:26a0: icmp_seq=1 ttl=64 time=0.420 ms

--- fd3c:be8a:173f:8e80:419:c082:e8cc:26a0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.420/0.420/0.420/0.000 ms
```
As we can observe, `sensor1` can ping `sensor2`.

Pinging `sensor1` to `sensor7`:
```
root@sensor1:/# ping -c1 fd3c:be8a:173f:8e80:3083:6218:aee4:e62d
PING fd3c:be8a:173f:8e80:3083:6218:aee4:e62d(fd3c:be8a:173f:8e80:3083:6218:aee4:e62d) 56 data bytes
64 bytes from fd3c:be8a:173f:8e80:3083:6218:aee4:e62d: icmp_seq=1 ttl=63 time=0.209 ms

--- fd3c:be8a:173f:8e80:3083:6218:aee4:e62d ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.209/0.209/0.209/0.000 ms
```
As we can observe, `sensor1` can ping `sensor7`.

Traceroute from `sensor1`:
```
root@sensor1:/# traceroute fd3c:be8a:173f:8e80:3083:6218:aee4:e62d
traceroute to fd3c:be8a:173f:8e80:3083:6218:aee4:e62d (fd3c:be8a:173f:8e80:3083:6218:aee4:e62d), 30 hops max, 80 byte packets
 1  fd3c:be8a:173f:8e80:419:c082:e8cc:26a0 (fd3c:be8a:173f:8e80:419:c082:e8cc:26a0)  0.319 ms  0.047 ms  0.034 ms
 2  fd3c:be8a:173f:8e80:3083:6218:aee4:e62d (fd3c:be8a:173f:8e80:3083:6218:aee4:e62d)  0.109 ms  0.063 ms  0.068 ms
```

Indeed, the traceroute command confirms that `sensor2` acts as an intermediate node in the communication path to `sensor7`. This shows how the routing protocol (like RPL) establishes paths through the network, using intermediate nodes to relay messages.

The traceroute output will reveal the sequence of nodes that the packets traverse, with `sensor2` appearing as a hop between `sensor7` and `sensor1` (or whichever node is initiating the communication). This behavior highlights the importance of intermediate nodes in enabling long-distance communication in networks where direct connections are not feasible due to range limitations.

Close Mininet-WPAN with the `exit` command.

### Use Case #3 - Energy Consumption

### based on the traffic data
Running the network topology:  
```
$ sudo python topology.py -b
```


After running the network topology, a terminal will open showing `sensor1` pinging `sensor2`. This ping sequence will continue until `sensor1` has sent 50 ICMP packets to `sensor2`, after which you can close the Mininet-WPAN cli with the exit command, and you will get the results below:  
```
energy consumed by sensor1: 6.351666666666667e-07 Wh
energy consumed by sensor2: 6.351666666666667e-07 Wh
energy consumed by sensor7: 5.927194444444446e-07 Wh
```

As observed, `sensor1` and `sensor2` exhibit higher battery consumption due to the increased packet exchange between them. This interaction demonstrates the impact of communication load on energy usage, highlighting the need for efficient power management in networks with limited battery resources. By monitoring this battery consumption, we can gain valuable insights into the energy demands of active sensor nodes, which is essential for optimizing network lifetime in IoT applications.


### based on the CPU usage
Running the network topology:  
```
$ sudo python topology.py -a
```

After 60 seconds the experiment will finish, and you can run the `graph.py` file to obtain the energy consumed by the CPU of the sensors.

```
python graph.py
```
![](https://raw.githubusercontent.com/ramonfontes/mn-wpan/refs/heads/main/figures/image3.png)

## LICENSE

Apache License Version 2.0, January 2004 http://www.apache.org/licenses/
