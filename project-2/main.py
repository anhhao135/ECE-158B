from mininet.log import lg, info
from mininet.net import Mininet
from mininet.link import TCIntf
from mininet.util import custom
from mininet.cli import CLI
import time
from fattree import FatTree

#parameters to define link behavior
DELAY = '1ms'
BW = 100

#define ping count in test
PING_COUNT = 100

def pingTest(net): #host A pings host B 100 times
    info("Ping test\n")
    hb1, hg1 = net.getNodeByName('hb1', 'hg1')
    pingStart = time.time() #start ping timer
    for i in range(PING_COUNT):
        net.ping((hb1, hg1))
        info(str(i) + "\n")
    #info(hb1.cmd('ping 10.0.0.5 -c ' + str(PING_COUNT) + ' > ping.txt')) #start a ping to host B via host A's shell, and dump log to file
    pingEnd = time.time()
    info("Ping took: " + str(pingEnd - pingStart) + " seconds.\n") #print out total ping time

def iPerfTest(net): #host A sends 100MB to host B
    info("iPerf test\n")
    hb1, hg1 = net.getNodeByName('hb1', 'hg1')
    hg1.cmd('iperf -s &') #start iperf server on host B
    iPerfStart = time.time()
    info(hb1.cmd('iperf -c 10.0.0.5 -n 100M -i 1 > iperf.txt')) #start file transfer from host A's shell to host B, and dump log to file
    iPerfEnd = time.time()
    info("100MB iPerf took: " + str(iPerfEnd - iPerfStart) + " seconds.\n") #print out total transfer time

def elephantAndMiceTest(net): #do both tests at the same time
    info("Elephant and mice test\n")
    hb1, hg1 = net.getNodeByName('hb1', 'hg1')
    hg1.cmd('iperf -s &') #start iperf server on host B
    info("Started iPerf\n")
    hb1.cmd('iperf -c 10.0.0.5 -n 100M -i 1 > iperfSimul.txt &') #start file transfer from host A, and dump log to file, but make it non-blocking with &
    info("Started pings\n")
    hb1.cmd('ping 10.0.0.5 -c ' + str(PING_COUNT) + ' > pingSimul.txt') #start pings from host A, and dump log to file, but make it blocking so we know when the pings are finished and we can inspect the log files

if __name__ == '__main__':
    lg.setLogLevel( 'info' ) #for print out debugging
    intf = custom(TCIntf, bw=BW, delay=DELAY) #define the link parameters for the entire network using the delay and bandwidth values
    network = Mininet(FatTree(), intf=intf, waitConnected=True) #instantiate a mininet with fat tree topology, the link parameters, and wait for all switches to connect to the controller before starting
    network.start() #start the network
    info("Waiting for STP to converge...\n") #STP needs time to populate the switches' forwarding tables correctly. on my machine, this took 35 seconds but may take shorter or longer
    time.sleep(35)

    #run the tests
    pingTest(network) #host A pings host B only
    iPerfTest(network) #host A transfers 100MB to host B only
    elephantAndMiceTest(network) #both tests above happen at the same time
    CLI(network)
    network.stop() #exit the mininet