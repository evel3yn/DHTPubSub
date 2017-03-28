# DHTPubSub
## DHT Register/Lookup in Publish-Subscribe using ZMQ and Mininet

### Introduce
In this assignment we will build upon Assignment #1. Keep all the properties supported by the publishers and subscribers from assignment #1 including the QoS properties. However, this time we will do things a bit differently by using a DHT ring of event services instead of a single, centralized event service. Publishers and subscribers will use register to send their topics and offered and requested QoS to any one of the DHT nodes they know of. The DHT logic should then route it to the correct DHT ring event service, which then stores the info.

You have two choices in doing the information dissemination. If you want to use the event service, the publisher will just send its publication to the event service node that was responsible for registering it. You should know this from the return value of the register () message. That event service then sends the info to the registered subscribers. Alternately, subscribers can do a “lookup” for a publisher who satisfies their needs and connects to that publisher under the hood (as part of the middleware layer). But you will need to handle failures of publishers.

Python has a package called hash_ring, which you can install using pip. Hash ring implements consistent hashing. Please see https://pypi.python.org/pypi/hash_ring for a simple sample code on how to use the hash function.

### Structure
This project consistes of three files: publisher.py, DHTServer.py, subscriber.py

### Arguments
The argument of publisher.py: strength, zipcode, all of the server IP

The argument of DHTServer.py: all of the server IP, first is its own IP

The argument of subscriber.py: filter, all of the server IP

### Sockets
In publisher.py file, we use socket(PUB) connect all server using 5556 port.

In DHTServer.py file, we use two sockets. socket(SUB), this socket bind all IP using port 5556; socket2(PUB), this socket bind all IP using port 5550

In subscriber.py file, we use two sockets. socket(SUB), connects to the server which stores the subscribed topic using port 5550; solverSocket(PUB), connects all servers except failed one using port 5556

### Message between hosts
before publisher failed, it will send the topic and string 'pubfailed' to all servers, servers will send it to subscribers who connects to them

before server failed, it will send its ip to subscriber who connects to the server.

when sub receive the message that a server failed, it will delete the the IP of the failed server and remap, then send the IP of failed server to other servers

when other server receive the message that a server failed, they will remap the hashring.
