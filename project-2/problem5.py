from mininet.log import lg, info
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topo import SingleSwitchTopo, LinearTopo
from mininet.topolib import TreeTopo
from mininet.link import TCIntf
from mininet.util import custom
from mininet.cli import CLI
import time

BW = 100
DELAY = '1ms'

def iPerfPairsTest(net):
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    pairs = [(h1, h2), (h1, h4), (h1, h3), (h2, h3), (h2, h4), (h3, h4)]
    for pair in pairs:
        net.iperf(pair)

def iPerfSimultaneousTest(net):
    hosts = net.hosts
    for host in hosts:
        host.cmd('iperf -s &')
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    h1.cmd('iperf -c 10.0.0.2 -d > log12.txt & iperf -c 10.0.0.3 -d > log13.txt &iperf -c 10.0.0.4 -d > log14.txt &')
    h4.cmd('iperf -c 10.0.0.2 -d > log42.txt & iperf -c 10.0.0.3 -d > log43.txt &')
    h2.cmd('iperf -c 10.0.0.3 -d> log23.txt &')
    time.sleep(15)
    h1.cmd('cat log12.txt log13.txt log14.txt log42.txt log43.txt log23.txt > log.txt')

def iPerfPingTest(net):
    hosts = net.hosts
    for host in hosts:
        host.cmd('iperf -s &')
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    info( "*** pinging before iPerf\n" )
    info(h1.cmd('ping 10.0.0.3 -c 5'))
    h1.cmd('iperf -c 10.0.0.2 -d & iperf -c 10.0.0.3 -d & iperf -c 10.0.0.4 -d &')
    info( "*** pinging during iPerf\n" )
    info(h1.cmd('ping 10.0.0.3 -c 5'))


if __name__ == '__main__':
    intf = custom(TCIntf, bw=BW, delay=DELAY)
    lg.setLogLevel( 'info' )
    OVSKernelSwitch.setup()

    network = Mininet(SingleSwitchTopo(k=4), switch=OVSKernelSwitch, waitConnected=True, intf=intf)
    #network = Mininet(LinearTopo(k=4), switch=OVSKernelSwitch, waitConnected=True, intf=intf)
    #network = Mininet(TreeTopo(depth=2, fanout=2), switch=OVSKernelSwitch, waitConnected=True, intf=intf)

    network.start()
    network.pingAll()
    
    #iPerfPairsTest(network)
    #iPerfSimultaneousTest(network)
    iPerfPingTest(network)
    CLI( net )

    network.stop()