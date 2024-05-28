from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet 
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
 
#link parameters
DELAY = '1ms'
BW = 100
 
class FatTree( Topo ):
	def build( self ):
		#add blue hosts
		hb1 = self.addHost('hb1') #host A
		hb2 = self.addHost('hb2')
		hb3 = self.addHost('hb3')
		hb4 = self.addHost('hb4')

		#add orange hosts
		ho1 = self.addHost('ho1')
		ho2 = self.addHost('ho2')
		ho3 = self.addHost('ho3')
		ho4 = self.addHost('ho4')

		#add green hosts
		hg1 = self.addHost('hg1') #host B
		hg2 = self.addHost('hg2')
		hg3 = self.addHost('hg3')
		hg4 = self.addHost('hg4')

		#add red hosts
		hr1 = self.addHost('hr1')
		hr2 = self.addHost('hr2')
		hr3 = self.addHost('hr3')
		hr4 = self.addHost('hr4') #host C

		#add edge switches
		s3001 = self.addSwitch('s3001')
		s3002 = self.addSwitch('s3002')
		s3003 = self.addSwitch('s3003')
		s3004 = self.addSwitch('s3004')
		s3005 = self.addSwitch('s3005')
		s3006 = self.addSwitch('s3006')
		s3007 = self.addSwitch('s3007')
		s3008 = self.addSwitch('s3008')

		#add aggregation switches
		s2001 = self.addSwitch('s2001')
		s2002 = self.addSwitch('s2002')
		s2003 = self.addSwitch('s2003')
		s2004 = self.addSwitch('s2004')
		s2005 = self.addSwitch('s2005')
		s2006 = self.addSwitch('s2006')
		s2007 = self.addSwitch('s2007')
		s2008 = self.addSwitch('s2008')

		#add core switches
		s1001 = self.addSwitch('s1001')
		s1002 = self.addSwitch('s1002')
		s1003 = self.addSwitch('s1003')
		s1004 = self.addSwitch('s1004')

		#edge to host links
		self.addLink(s3001, hb1, bw=BW, delay=DELAY)
		self.addLink(s3001, hb2, bw=BW, delay=DELAY)
		self.addLink(s3002, hb3, bw=BW, delay=DELAY)
		self.addLink(s3002, hb4, bw=BW, delay=DELAY)
		
		self.addLink(s3003, ho1, bw=BW, delay=DELAY)
		self.addLink(s3003, ho2, bw=BW, delay=DELAY)
		self.addLink(s3004, ho3, bw=BW, delay=DELAY)
		self.addLink(s3004, ho4, bw=BW, delay=DELAY)

		self.addLink(s3005, hg1, bw=BW, delay=DELAY)
		self.addLink(s3005, hg2, bw=BW, delay=DELAY)
		self.addLink(s3006, hg3, bw=BW, delay=DELAY)
		self.addLink(s3006, hg4, bw=BW, delay=DELAY)

		self.addLink(s3007, hr1, bw=BW, delay=DELAY)
		self.addLink(s3007, hr2, bw=BW, delay=DELAY)
		self.addLink(s3008, hr3, bw=BW, delay=DELAY)
		self.addLink(s3008, hr4, bw=BW, delay=DELAY)
		
		#aggregation to edge links
		self.addLink(s2001, s3001, bw=BW, delay=DELAY)
		self.addLink(s2001, s3002, bw=BW, delay=DELAY)
		self.addLink(s2002, s3001, bw=BW, delay=DELAY)
		self.addLink(s2002, s3002, bw=BW, delay=DELAY)
		
		self.addLink(s2003, s3003, bw=BW, delay=DELAY)
		self.addLink(s2003, s3004, bw=BW, delay=DELAY)
		self.addLink(s2004, s3003, bw=BW, delay=DELAY)
		self.addLink(s2004, s3004, bw=BW, delay=DELAY)

		self.addLink(s2005, s3005, bw=BW, delay=DELAY)
		self.addLink(s2005, s3006, bw=BW, delay=DELAY)
		self.addLink(s2006, s3005, bw=BW, delay=DELAY)
		self.addLink(s2006, s3006, bw=BW, delay=DELAY)

		self.addLink(s2007, s3007, bw=BW, delay=DELAY)
		self.addLink(s2007, s3008, bw=BW, delay=DELAY)
		self.addLink(s2008, s3007, bw=BW, delay=DELAY)
		self.addLink(s2008, s3008, bw=BW, delay=DELAY)
		
		#core to aggregation links
		self.addLink(s1001, s2001, bw=BW, delay=DELAY)
		self.addLink(s1001, s2003, bw=BW, delay=DELAY)
		self.addLink(s1001, s2005, bw=BW, delay=DELAY)
		self.addLink(s1001, s2007, bw=BW, delay=DELAY)
		
		self.addLink(s1002, s2001, bw=BW, delay=DELAY)
		self.addLink(s1002, s2003, bw=BW, delay=DELAY)
		self.addLink(s1002, s2005, bw=BW, delay=DELAY)
		self.addLink(s1002, s2007, bw=BW, delay=DELAY)
		
		self.addLink(s1003, s2002, bw=BW, delay=DELAY)
		self.addLink(s1003, s2004, bw=BW, delay=DELAY)
		self.addLink(s1003, s2006, bw=BW, delay=DELAY)
		self.addLink(s1003, s2008, bw=BW, delay=DELAY)
		
		self.addLink(s1004, s2002, bw=BW, delay=DELAY)
		self.addLink(s1004, s2004, bw=BW, delay=DELAY)
		self.addLink(s1004, s2006, bw=BW, delay=DELAY)
		self.addLink(s1004, s2008, bw=BW, delay=DELAY)


topos = {
	'fattree':FatTree
}

