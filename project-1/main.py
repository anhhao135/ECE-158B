from lib import *
import matplotlib.pyplot as plt
import numpy as np

lowerBandwidth = 1
higherBandwidth = 5000
numberOfPeers = 100
peers = {}

fileNumberOfChunks = 100
torrentFileChunks = []
for i in range(fileNumberOfChunks):
    chunk = str(i)
    torrentFileChunks.append(chunk)

tracker = (torrentFileChunks, []) #tracker is tuple of (file size in chunks, list of peer IDs)

#create the source file peer    
sourcePeer = Peer(-1, higherBandwidth, peers, tracker, torrentFileChunks)
#peers[-1] = sourcePeer

for i in range(numberOfPeers):
    #peers[i] = Peer(i, random.randint(lowerBandwidth,higherBandwidth), peers, tracker, random.sample(torrentFileChunks, random.randint(0,fileNumberOfChunks - 1)))
    peers[i] = Peer(i, random.randint(lowerBandwidth,higherBandwidth), peers, tracker, random.sample(torrentFileChunks, 10))

for peerIndex, peer in peers.items():
    peer.joinTracker()
    peer.updateMissingChunks()

    

#peers[2].leaveTracker()

print(tracker)


#for peerIndex, peer in peers.items():
    #peer.print()


rarestChunkRequestPeriod = 5
topPeersRefreshPeriod = 10
optimisticUnchokePeriod = 30
simulationTime = 1000

percentageTrackers = {}
for peerIndex, peer in peers.items():
    percentageTrackers[peerIndex] = []

for t in range(1,simulationTime):
    print(t)
    if t % rarestChunkRequestPeriod == 0:
        for peerIndex, peer in peers.items():
            peer.requestRarestChunkFromPeers()

    for peerIndex, peer in peers.items():
        peer.sendChunksToTopPeers(t)
    
    for peerIndex, peer in peers.items():
        peer.processReceiveBuffer()

    if t % topPeersRefreshPeriod == 0:
            for peerIndex, peer in peers.items():
                peer.refreshTopPeers()

    if t % optimisticUnchokePeriod == 0:
            for peerIndex, peer in peers.items():
                peer.optimisticallyUnchokePeer()

    for peerIndex, peer in peers.items():
        percentage = peer.getDownloadPercentage()
        percentageTrackers[peerIndex].append(peer.getDownloadPercentage())
        #if (int(percentage) == 100) and (peer in tracker[1]):
        #     print("leaving!")
        #     peer.leaveTracker()
        


plt.figure()
for peerIndex, peer in peers.items():
    plt.plot(np.array(percentageTrackers[peerIndex]), label = str(peerIndex))
plt.legend()
plt.show()

