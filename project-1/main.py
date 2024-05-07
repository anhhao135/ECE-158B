from lib import *

lowerBandwidth = 1
higherBandwidth = 5000
numberOfPeers = 10
peers = {}

fileNumberOfChunks = 50
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

#for peerIndex, peer in peers.items():
    #peer.print()

for i in range(1,10000):
    for peerIndex, peer in peers.items():
        #peer.refreshTopPeers()
        peer.requestRarestChunkFromPeers()
        #peer.sendChunkToPeer('1', 10, 2)

    for peerIndex, peer in peers.items():
        peer.print()
        
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOO00000000000000000000000000000000000000000000OOOOOOOOOOOOOOOOO")

    for peerIndex, peer in peers.items():
        peer.sendChunksToTopPeers()

    for peerIndex, peer in peers.items():
        peer.print()
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOO00000000000000000000000000000000000000000000OOOOOOOOOOOOOOOOO")

    for peerIndex, peer in peers.items():
        peer.processReceiveBuffer()

    for peerIndex, peer in peers.items():
        peer.print()
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOO00000000000000000000000000000000000000000000OOOOOOOOOOOOOOOOO")
    if i % 5 == 0:
        print("reevaluating!!!")
        for peerIndex, peer in peers.items():
            peer.refreshTopPeers()

    for peerIndex, peer in peers.items():
        peer.print()
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOO00000000000000000000000000000000000000000000OOOOOOOOOOOOOOOOO")
    if (i+8) % 5 == 0:
        print("unchoking!!!!")
        for peerIndex, peer in peers.items():
            peer.optimisticallyUnchokePeer()
    input("Press Enter to continue...")