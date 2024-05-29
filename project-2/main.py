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
 

def pingTest(net):
    info("Ping test\n")
    hb1 = net.getNodeByName('hb1')
    pingStart = time.time()
    info(hb1.cmd('ping 10.0.0.5 -c 10'))
    pingEnd = time.time()
    info("Ping took: " + str(pingEnd - pingStart) + " seconds.")


if __name__ == '__main__':
    intf = custom(TCIntf, bw=BW, delay=DELAY)
    lg.setLogLevel( 'info' )

    #network = Mininet(FatTree, switch=OVSKernelSwitch, waitConnected=True, intf=intf)
    network = Mininet(FatTree(), intf=intf, waitConnected=True)

    network.start()
    info("Waiting for STP to converge...\n")
    time.sleep(35)

    pingTest(network)
    #network.pingAll()

    CLI( network )

    network.stop()