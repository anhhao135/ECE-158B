from lib import *
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

#BitTorrent simulator for ECE 158B SP24 project 1
#Hao Le A15547504

#running this is meant to show a simple Torrent simulation run but not replicate every type of scenario discussed in the report

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


for i in range(NUM_PEERS): #we create the other peers
    peers[i] = Peer(i, random.randint(LOW_BANDWIDTH, HIGH_BANDWIDTH), peers, tracker, [])
    #each peer will have a randomly selected bandwidth from a low to high range, and no chunks acquired to start with
    #however, we can specify if a peer starts out already with some chunks of the torrent; this can enhance its download rate

    peers[i].joinTracker(0) #each peer will join the tracker before the simulation starts
    #but we can also specify a peer to join midway through the simulation by calling joinTracker() at a specific time step

#these lists are to track the order at which peers finish and their corresponding bandwidths
#this will illustrate how BitTorrent establishes fairness amongst hetereogeneous peers
finisherBandwidths = []
finisherIPs = []

#this is to track the download progress of each peer to be plotted later
percentageTrackers = {}
for peerIndex, peer in peers.items():
    percentageTrackers[peerIndex] = []

#this is to track the download rate of each peer to be plotted later
rateTrackers = {}
for peerIndex, peer in peers.items():
    rateTrackers[peerIndex] = []


#main simulation loop
#implemented as a round-robin schedule that executes routines at different intervals
#mimicking the periodic actions a real BitTorrent peer would do under the hood

for t in tqdm(range(0,SIMULATION_TIME)): #we run the simulation up to a specified end time

    random.shuffle(tracker[1])

    #here we can trigger the source peer to leave at time step 1500
    #this is an example but can be done for any routine such as peers coming and going
    #if t == int(1500):
        #peers[-1].leaveTracker()

    #below are peer routines that occur at specified intervals
    #we can modify the intervals in lib.py to change the simulation behavior

    if t % RAREST_CHUNK_REQUEST_PERIOD == 0: #query if it is time for each peer to request the rarest chunk; the interval can be customized
        for peerIndex in tracker[1]: #iterate through all the peers that are part of the tracker and therefore choose to participate in the Torrent
            peers[peerIndex].requestRarestChunkFromPeers() #call the rare chunk request routine

    for peerIndex in tracker[1]: #each peer is to flush out its inbox of chunks and update its missing chunks every simulation time step; this is done as frequently as possible since it is not dependent on bandwidth and stays local to a peer's hardware
        peers[peerIndex].processReceiveBuffer()

    for peerIndex in tracker[1]: #the routine for sending chunks to top peers IS bandwidth dependent, hence we cannot specify a fixed interval for all peers
        peers[peerIndex].sendChunksToTopPeers(t) #instead, we call the routine every time step but pass in the time value so it is up to the peer's discretion to decide if it is within its bandwidth to send
        #this is adequate to mimick a real life bandwidth constraint
    
    if t % TOP_PEERS_REFRESH_PERIOD == 0: #fixed interval routine for each peer to reevaluate its top 4 peers; this parameter can be customized in lib.py
        for peerIndex in tracker[1]:
            peers[peerIndex].refreshTopPeers()

    if t % OPTIMISTIC_UNCHOKE_PERIOD == 0: #fixed interval routine for each peer to optimistically unchoke a free rider; this parameter can be customized in lib.py and should be less frequent than the top peers refresh frequency to accurately model BitTorrent
            for peerIndex in tracker[1]:
                peers[peerIndex].optimisticallyUnchokePeer()



    #the rest of the loop is for adding data points to measure the performance of each peer and the Torrent as a whole

    for peerIndex, peer in peers.items():
        percentage = peer.getDownloadPercentage() #get the current download % of each peer
        if percentage == 100:
            if peerIndex not in finisherIPs:
                finisherIPs.append(peerIndex) #if the peer has just finished and reached 100%, add it to the finishers list to track the order
                finisherBandwidths.append(peer.bandwidth)
                if peerIndex != -1 and LEAVE_WHEN_DONE: #control the churning behavior of a peer
                    peer.leaveTracker() #if a peer is not a source peer and is finished, it can leave if specified by the parameter

        percentageTrackers[peerIndex].append(percentage) #track the download progress of each peer

        if (t % DOWNLOAD_RATE_WINDOW == 0): #calculate the instantaneous download rate of each peer over a finite window and track it
            rate = peer.getDownloadRate(t)
            rateTrackers[peerIndex].append(rate)


#plot different measurements of the Torrent simulation

#plot the download progress for each peer over time
plt.figure()
for peerIndex, peer in peers.items():
    if peerIndex != -1: #do not plot the already finished source peer
        plt.plot(np.array(percentageTrackers[peerIndex]), label = "IP: " + str(peerIndex) + "|Bandwidth: " + str(peer.bandwidth))
plt.legend()
plt.title("Peer Download Percentage Over Time")
plt.xlabel("Time")
plt.ylabel("Download %")
plt.ylim(0, 105)

#plot the peer finishing order vs. the bandwidth
#to illustrate how BitTorrent rewards higher upload bandwidth with faster download rates
plt.figure()
plt.plot(finisherBandwidths)
plt.title("Finishing Order vs. Peer Upload Bandwidth")
plt.xlabel("Finishing Order")
plt.ylabel("Upload Bandwidth")

#plot the maximum recorded download rate for each peer
plt.figure()
plt.title("Maximum Per-Peer Download Rate")
plt.xlabel("Peer IP")
plt.ylabel("Chunks / Time Unit")
for peerIndex, peer in peers.items():
    if peerIndex != -1:
        print()
        plt.scatter(peerIndex, np.max(np.array(rateTrackers[peerIndex])))

plt.show() #display the plots


