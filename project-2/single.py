#!/usr/bin/env python

"""
This example shows how to create a network and run multiple tests.
For a more complicated test example, see udpbwtest.py.
"""

from mininet.cli import CLI
from mininet.log import lg, info
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topo import SingleSwitchTopo
from mininet.link import TCIntf
from mininet.util import custom
import time

BW = 100
DELAY = '1ms'

def ifconfigTest( net ):
    "Run ifconfig on all hosts in net."
    hosts = net.hosts
    for host in hosts:
        info( host.cmd( 'ifconfig' ) )

def iPerfPairsTest(net):
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    pairs = [(h1, h2), (h1, h4), (h1, h3), (h2, h3), (h2, h4), (h3, h4)]
    for pair in pairs:
        net.iperf(pair)

def iPerfSimultaneousTest(net):
    hosts = net.hosts
    for host in hosts:
        info(host.cmd('ifconfig'))
        info(host.cmd('iperf -s &'))
    time.sleep(1)
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    info(h1.cmd('iperf -c h4'))

    


if __name__ == '__main__':
    intf = custom(TCIntf, bw=BW, delay=DELAY)
    lg.setLogLevel( 'info' )
    info( "*** Initializing Mininet and kernel modules\n" )
    OVSKernelSwitch.setup()
    info( "*** Creating network\n" )
    network = Mininet(SingleSwitchTopo(k=4), switch=OVSKernelSwitch,
                       waitConnected=True, intf=intf)
    info( "*** Starting network\n" )
    network.start()
    info( "*** Running ping test\n" )
    network.pingAll()
    info( "*** Running iPerf pair tests\n" )
    #iPerfPairsTest(network)
    iPerfSimultaneousTest(network)
    info( "*** Starting CLI (type 'exit' to exit)\n" )
    CLI( network )
    info( "*** Stopping network\n" )
    network.stop()