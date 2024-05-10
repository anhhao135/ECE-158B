from lib import *
import matplotlib.pyplot as plt
import numpy as np

lowerBandwidth = 10
higherBandwidth = 1000
numberOfPeers = 5
peers = {}

fileNumberOfChunks = 50
torrentFileChunks = []
for i in range(fileNumberOfChunks):
    chunk = str(i)
    torrentFileChunks.append(chunk)

tracker = (torrentFileChunks, []) #tracker is tuple of (file size in chunks, list of peer IDs)


#create the source file peer    
#sourcePeer = Peer(-1, higherBandwidth, peers, tracker, torrentFileChunks)
#peers[-1] = sourcePeer



for i in range(numberOfPeers):
    #peers[i] = Peer(i, random.randint(lowerBandwidth,higherBandwidth), peers, tracker, random.sample(torrentFileChunks, random.randint(0,fileNumberOfChunks - 1)))
    peers[i] = Peer(i, random.randint(lowerBandwidth,higherBandwidth), peers, tracker, random.sample(torrentFileChunks,30))


#peers[-1] = Peer(-1, 6, peers, tracker, torrentFileChunks[:5])
#peers[0] = Peer(0, 9, peers, tracker, torrentFileChunks[4:10])
#peers[1] = Peer(1, 50, peers, tracker, torrentFileChunks[8:])
#peers[2] = Peer(2, 10, peers, tracker, torrentFileChunks[:])
#peers[3] = Peer(3, 10, peers, tracker, [])

#peers[-1] = Peer(-1, 1000, peers, tracker, torrentFileChunks[:25])
#peers[0] = Peer(0, 1000, peers, tracker, torrentFileChunks[23:])
#peers[1] = Peer(1, 100, peers, tracker, torrentFileChunks[10:17])
#peers[2] = Peer(2, 1000, peers, tracker, torrentFileChunks[15:22])
#peers[3] = Peer(3, 200, peers, tracker, torrentFileChunks[20:])
#peers[4] = Peer(4, 10, peers, tracker, torrentFileChunks[:10])


for peerIndex, peer in peers.items():
    peer.joinTracker()
    peer.updateMissingChunks()

rarestChunkRequestPeriod = 5
topPeersRefreshPeriod = 10
optimisticUnchokePeriod = 30


clearRequestBufferPeriod = 5000
simulationTime = 2000

percentageTrackers = {}
for peerIndex, peer in peers.items():
    percentageTrackers[peerIndex] = []

for t in range(1,simulationTime):

    #l = list(peers.items())
    #random.shuffle(l)
    #peers = dict(l)

    print(t)

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
    if t % clearRequestBufferPeriod == 0:
            for peerIndex, peer in peers.items():
                peer.clearRequestBuffer()


    for peerIndex, peer in peers.items():
        percentage = peer.getDownloadPercentage()
        percentageTrackers[peerIndex].append(peer.getDownloadPercentage())
        #if peerIndex == 0:
        peer.print()
        #if (int(percentage) == 100) and (peer in tracker[1]):
        #     print("leaving!")
        #     peer.leaveTracker()
    #print("Press any key to continue...")
    input()
        


plt.figure()
for peerIndex, peer in peers.items():
    plt.plot(np.array(percentageTrackers[peerIndex]), label = str(peerIndex) + "/" + str(peer.bandwidth))
plt.legend()
plt.show()

