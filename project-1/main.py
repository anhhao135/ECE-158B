from lib import *
import matplotlib.pyplot as plt
import numpy as np
from labellines import labelLines
from tqdm import tqdm

#BitTorrent simulator for ECE 158B SP24 project 1
#Hao Le A15547504

peers = {} #use dictionary to define peer list where index is the peer's IP address, and the returned object is of Peer class   

#create the torrent source file chunks, just a list of incrementing strings of numbers up to the specified chunk amount
torrentFileChunks = []
for i in range(NUM_CHUNKS):
    chunk = str(i)
    torrentFileChunks.append(chunk)

tracker = (torrentFileChunks, []) #torrent tracker is tuple of (list of complete source file chunks, list of peer IDs)
#any peer part of the tracker can view other peers participating in the torrent as well as what the source file's chunks are - this is to compare with its own acquired chunks and discern what is missing

#the first peer we make is the source peer that seeds the original chunks of the file to the network
peers[-1] = Peer(-1, HIGH_BANDWIDTH, peers, tracker, torrentFileChunks)
peers[-1].joinTracker(0) #join the tracker before the simulation starts
#the source peer has IP address -1, has the highest possible bandwidth, and all the source file chunks already acquired


for i in range(NUM_PEERS): #we create the other peers of the torrent0
    peers[i] = Peer(i, random.randint(LOW_BANDWIDTH,HIGH_BANDWIDTH), peers, tracker, random.sample(torrentFileChunks, 50))
    #peers[i] = Peer(i, int(HIGH_BANDWIDTH / 10), peers, tracker, [])
    #peers[i].joinTracker(0)
    #each peer will have a randomly selected bandwidth from a low to high range, and no chunks acquired to start with
finisherBandwidths = []
finisherIPs = []

percentageTrackers = {}
for peerIndex, peer in peers.items():
    percentageTrackers[peerIndex] = []

rateTrackers = {}
for peerIndex, peer in peers.items():
    rateTrackers[peerIndex] = []

peerJoinTracker = 0

for t in tqdm(range(0,SIMULATION_TIME)):

    random.shuffle(tracker[1])

    if t % 200 == 0 and peerJoinTracker < NUM_PEERS:
        peers[peerJoinTracker].joinTracker(t)
        peerJoinTracker = peerJoinTracker + 1


    #if t == int(1500):
    #    peers[-1].joinTracker(t)

    #if t == int(1500):
        #peers[-1].leaveTracker()

    #l = list(peers.items())
    #random.shuffle(l)
    #peers = dict(l)

    #print(t)

    if t % RAREST_CHUNK_REQUEST_PERIOD == 0:
        for peerIndex in tracker[1]:
            peers[peerIndex].requestRarestChunkFromPeers()

    for peerIndex in tracker[1]:
        peers[peerIndex].processReceiveBuffer()

    for peerIndex in tracker[1]:
        peers[peerIndex].sendChunksToTopPeers(t)

    
    for peerIndex, peer in peers.items():
        peer.processReceiveBuffer()

    if t % TOP_PEERS_REFRESH_PERIOD == 0:
        for peerIndex in tracker[1]:
            peers[peerIndex].refreshTopPeers()

    if t % OPTIMISTIC_UNCHOKE_PERIOD == 0:
            for peerIndex in tracker[1]:
                peers[peerIndex].optimisticallyUnchokePeer()



    for peerIndex, peer in peers.items():
        percentage = peer.getDownloadPercentage()
        if percentage == 100:
            if peerIndex not in finisherIPs:
                finisherIPs.append(peerIndex)
                finisherBandwidths.append(peer.bandwidth)
                if peerIndex != -1 and LEAVE_WHEN_DONE:
                    peer.leaveTracker()

        percentageTrackers[peerIndex].append(percentage)
        if (t % DOWNLOAD_RATE_WINDOW == 0):
            rate = peer.getDownloadRate(t)
            rateTrackers[peerIndex].append(rate)
        #if peerIndex == 0:
        #peer.print()
        #if (int(percentage) == 100) and (peer in tracker[1]):
        #     print("leaving!")
        #     peer.leaveTracker()
    #print("Press any key to continue...")
    #input()



plt.figure()
for peerIndex, peer in peers.items():
    if NUM_PEERS < 20 and peerIndex != -1:
        plt.plot(np.array(percentageTrackers[peerIndex]), label = "IP: " + str(peerIndex) + "|Bandwidth: " + str(peer.bandwidth))
    elif peerIndex != -1 and peerIndex % NUM_PEERS_PLOT == 0:
        plt.plot(np.array(percentageTrackers[peerIndex]), label = "IP: " + str(peerIndex) + "|Bandwidth: " + str(peer.bandwidth))
plt.legend()
plt.title("Peer Download Percentage Over Time")
plt.xlabel("Time")
plt.ylabel("Download %")
plt.ylim(0, 105)
#lines = plt.gca().get_lines()
#labelLines(lines, align=True)


plt.figure()
plt.plot(finisherBandwidths)
plt.title("Finishing Order vs. Peer Upload Bandwidth")
plt.xlabel("Finishing Order")
plt.ylabel("Upload Bandwidth")


plt.figure()
for peerIndex, peer in peers.items():
    if peerIndex != -1:
        plt.plot(np.array(percentageTrackers[peerIndex]))
plt.legend()
plt.title("Peer Download Percentage Over Time")
plt.xlabel("Time")
plt.ylabel("Download %")
plt.ylim(0, 105)


plt.figure()
plt.title("Peer 5 Effective Download Rate Over Time")
plt.xlabel("Time x 100")
plt.ylabel("Chunks / Time Unit")
plt.plot(rateTrackers[5])



plt.show()


