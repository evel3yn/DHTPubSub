import zmq
import sys
from hash_ring import HashRing

context = zmq.Context()
socket = context.socket(zmq.SUB)

#send the ip of all server
addStr=[]
for i in range(2,len(sys.argv)):
    srv_addr = sys.argv[i]
    addStr.append("tcp://" + srv_addr + ":5556")

#hashring
ring = HashRing(addStr)

#filter
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

server = ring.get_node(zip_filter)

print("Collecting updates from weather server...")
socket.connect(server)


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
#5 seconds
evit = poller.poll(5000)

while True:
    zip = tem = rel = ['', '', '', '', '']
    zipInt = temInt = relInt = [0, 0, 0, 0, 0]

    i = 0
    print("ready to receive")
    #if there is anything to receive
    if evit:
        string = socket.recv()
        print("message received")

        zipcodeStr, temperatureStr, relhumidityStr, strengthStr, zipHisStr, temHisStr, relHisStr = string.split()
        # receive history
        zip[0], zip[1], zip[2], zip[3], zip[4] = zipHisStr.split("/")
        tem[0], tem[1], tem[2], tem[3], tem[4] = temHisStr.split("/")
        rel[0], rel[1], rel[2], rel[3], rel[4] = relHisStr.split("/")

        # turn the string to int
        for k in range(5):
            zipInt[k] = int(zip[k])
            temInt[k] = int(tem[k])
            relInt[k] = int(rel[k])

        print("This is received history")
        a = 1
        for l in range(0, 5):
            # if zipInt[l] == int(zip_filter):
            print("%ith temperature is %i" % (a, temInt[l]))
            print("%ith relhumidity is %i" % (a, relInt[l]))
            a += 1

        print('This is received message')
        print("Topic: %s, Temperature: %s, Humidity: %s, Strength: %s" % (
            zipcodeStr, temperatureStr, relhumidityStr, strengthStr))
    #if timeout
    else:
        print("can't receive message")
        solverSocket=context.socket(zmq.PUB)
        solverSocket.connect(server)
        msg='999'
        socket.send_string(msg)







