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
 

if __name__ == '__main__':
    intf = custom(TCIntf, bw=BW, delay=DELAY)
    lg.setLogLevel( 'info' )

    #network = Mininet(FatTree, switch=OVSKernelSwitch, waitConnected=True, intf=intf)
    network = Mininet(FatTree(), intf=intf, waitConnected=True)

    network.start()
    #network.pingAll()

    CLI( network )

    network.stop()