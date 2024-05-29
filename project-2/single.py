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
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    info(h1.cmd('iperf -c 10.0.0.2 -d > log12.txt & iperf -c 10.0.0.3 -d > log13.txt &iperf -c 10.0.0.4 -d > log14.txt &'))
    info(h4.cmd('iperf -c 10.0.0.2 -d > log42.txt & iperf -c 10.0.0.3 -d > log43.txt &'))
    info(h2.cmd('iperf -c 10.0.0.3 -d> log23.txt &'))
    time.sleep(15)
    info(h1.cmd('cat log12.txt log13.txt log14.txt log42.txt log43.txt log23.txt > log.txt'))

    


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
    info( "*** Running iPerf tests\n" )
    iPerfPairsTest(network)
    iPerfSimultaneousTest(network)
    network.stop()