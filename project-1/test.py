import random
from natsort import natsorted

class Peer:
    def __init__(self, IPAddress, bandwidth, peers, tracker, acquiredChunks):
        self.IPAddress = IPAddress
        self.bandwidth = bandwidth
        self.peers = peers
        self.tracker = tracker
        self.acquiredChunks = acquiredChunks
        self.torrentSourceChunks = None
        self.receiveBuffer = []
        self.missingChunks = None
        self.downloadBandwidths = {}
        self.uploadBandwidths = {}
        self.top4Peers = []

    def refreshTop4Peers(self):
        trackerPeers = self.tracker[1].copy()
        trackerPeers.remove(self.IPAddress)
        self.top4Peers = random.sample(trackerPeers, 4)

    def joinTracker(self):
        self.tracker[1].append(self.IPAddress)
        self.torrentSourceChunks = self.tracker[0]
    
    def leaveTracker(self):
        self.tracker[1].remove(self.IPAddress)

    def updateMissingChunks(self):
        self.missingChunks = list(set(self.torrentSourceChunks).difference(self.acquiredChunks))

    def sendRandomHellos(self):
        for peerID in tracker[1]:
            if peerID != self.IPAddress:
                peers[peerID].receiveBuffer.append("hello from " + str(self.IPAddress))

    def print(self):
        print("--------")
        print("IP: " + str(self.IPAddress))
        print("Bandwidth: " + str(self.bandwidth))
        print("Acquired chunks: " + str(natsorted(self.acquiredChunks)))
        print("Receive buffer: " + str(self.receiveBuffer))
        print("Missing chunks: " + str(natsorted(self.missingChunks)))
        print("Top 4 peers: " + str(natsorted(self.top4Peers)))
        print("--------")


lowerBandwidth = 1
higherBandwidth = 1000
numberOfPeers = 6
peers = {}

fileNumberOfChunks = 10
torrentFileChunks = []
for i in range(fileNumberOfChunks):
    chunk = str(i)
    torrentFileChunks.append(chunk)

tracker = (torrentFileChunks, []) #tracker is tuple of (file size in chunks, list of peer IDs)

#create the source file peer    
sourcePeer = Peer(-1, higherBandwidth, peers, tracker, torrentFileChunks)
peers[-1] = sourcePeer

for i in range(numberOfPeers):
    peers[i] = Peer(i, random.randint(lowerBandwidth,higherBandwidth), peers, tracker, random.sample(torrentFileChunks, random.randint(0,fileNumberOfChunks - 1)))

for peerIndex, peer in peers.items():
    peer.joinTracker()
    peer.updateMissingChunks()

#peers[2].leaveTracker()

print(tracker)

for peerIndex, peer in peers.items():
    peer.sendRandomHellos()
    peer.refreshTop4Peers()

for peerIndex, peer in peers.items():
    peer.print()