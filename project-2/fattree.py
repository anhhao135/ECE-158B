from mininet.topo import Topo

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
		hr4 = self.addHost('hr4')

		#add edge switches
		s3001 = self.addSwitch('s3001', stp=True, failMode='standalone')
		s3002 = self.addSwitch('s3002', stp=True, failMode='standalone')
		s3003 = self.addSwitch('s3003', stp=True, failMode='standalone')
		s3004 = self.addSwitch('s3004', stp=True, failMode='standalone')
		s3005 = self.addSwitch('s3005', stp=True, failMode='standalone')
		s3006 = self.addSwitch('s3006', stp=True, failMode='standalone')
		s3007 = self.addSwitch('s3007', stp=True, failMode='standalone')
		s3008 = self.addSwitch('s3008', stp=True, failMode='standalone')

		#add aggregation switches
		s2001 = self.addSwitch('s2001', stp=True, failMode='standalone')
		s2002 = self.addSwitch('s2002', stp=True, failMode='standalone')
		s2003 = self.addSwitch('s2003', stp=True, failMode='standalone')
		s2004 = self.addSwitch('s2004', stp=True, failMode='standalone')
		s2005 = self.addSwitch('s2005', stp=True, failMode='standalone')
		s2006 = self.addSwitch('s2006', stp=True, failMode='standalone')
		s2007 = self.addSwitch('s2007', stp=True, failMode='standalone')
		s2008 = self.addSwitch('s2008', stp=True, failMode='standalone')

		#add core switches
		s1001 = self.addSwitch('s1001', stp=True, failMode='standalone')
		s1002 = self.addSwitch('s1002', stp=True, failMode='standalone')
		s1003 = self.addSwitch('s1003', stp=True, failMode='standalone')
		s1004 = self.addSwitch('s1004', stp=True, failMode='standalone')

		#edge to host links
		self.addLink(s3001, hb1)
		self.addLink(s3001, hb2)
		self.addLink(s3002, hb3)
		self.addLink(s3002, hb4)
		
		self.addLink(s3003, ho1)
		self.addLink(s3003, ho2)
		self.addLink(s3004, ho3)
		self.addLink(s3004, ho4)

		self.addLink(s3005, hg1)
		self.addLink(s3005, hg2)
		self.addLink(s3006, hg3)
		self.addLink(s3006, hg4)

		self.addLink(s3007, hr1)
		self.addLink(s3007, hr2)
		self.addLink(s3008, hr3)
		self.addLink(s3008, hr4)
		
		#aggregation to edge links
		self.addLink(s2001, s3001)
		self.addLink(s2001, s3002)
		self.addLink(s2002, s3001)
		self.addLink(s2002, s3002)
		
		self.addLink(s2003, s3003)
		self.addLink(s2003, s3004)
		self.addLink(s2004, s3003)
		self.addLink(s2004, s3004)

		self.addLink(s2005, s3005)
		self.addLink(s2005, s3006)
		self.addLink(s2006, s3005)
		self.addLink(s2006, s3006)

		self.addLink(s2007, s3007)
		self.addLink(s2007, s3008)
		self.addLink(s2008, s3007)
		self.addLink(s2008, s3008)
		
		#core to aggregation links
		self.addLink(s1001, s2001)
		self.addLink(s1001, s2003)
		self.addLink(s1001, s2005)
		self.addLink(s1001, s2007)
		
		self.addLink(s1002, s2001)
		self.addLink(s1002, s2003)
		self.addLink(s1002, s2005)
		self.addLink(s1002, s2007)
		
		self.addLink(s1003, s2002)
		self.addLink(s1003, s2004)
		self.addLink(s1003, s2006)
		self.addLink(s1003, s2008)
		
		self.addLink(s1004, s2002)
		self.addLink(s1004, s2004)
		self.addLink(s1004, s2006)
		self.addLink(s1004, s2008)


topos = {
	'fattree':FatTree
}

