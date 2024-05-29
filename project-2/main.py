from mininet.log import lg, info
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topo import SingleSwitchTopo, LinearTopo
from mininet.topolib import TreeTopo
from mininet.link import TCIntf, TCLink
from mininet.util import custom
import time
from fattree import FatTree
from mininet.cli import CLI


DELAY = '1ms'
BW = 100
PING_COUNT = 20
 

def pingTest(net):
    info("Ping test\n")
    hb1 = net.getNodeByName('hb1')
    pingStart = time.time()
    info(hb1.cmd('ping 10.0.0.5 -c ' + str(PING_COUNT)))
    pingEnd = time.time()
    info("Ping took: " + str(pingEnd - pingStart) + " seconds.\n")

def iPerfTest(net):
    info("iPerf test\n")
    hb1, hg1 = net.getNodeByName('hb1', 'hg1')
    hg1.cmd('iperf -s &')
    iPerfStart = time.time()
    info(hb1.cmd('iperf -c 10.0.0.5 -n 100M'))
    iPerfEnd = time.time()
    info("100MB iPerf took: " + str(iPerfEnd - iPerfStart) + " seconds.\n")

def elephantAndMiceTest(net):
    info("Elephant and mice test\n")
    hb1, hg1 = net.getNodeByName('hb1', 'hg1')
    hg1.cmd('iperf -s &')
    hb1.cmd('ping 10.0.0.5 -c ' + str(PING_COUNT) + ' > ping.txt &')
    hb1.cmd('iperf -c 10.0.0.5 -n 100M > iperf.txt &')

if __name__ == '__main__':
    intf = custom(TCIntf, bw=BW, delay=DELAY)
    lg.setLogLevel( 'info' )

    #network = Mininet(FatTree, switch=OVSKernelSwitch, waitConnected=True, intf=intf)
    network = Mininet(FatTree(), intf=intf, waitConnected=True)

    network.start()
    info("Waiting for STP to converge...\n")
    time.sleep(35)

    pingTest(network)
    iPerfTest(network)
    elephantAndMiceTest(network)
    #network.pingAll()

    CLI( network )

    network.stop()