import random
from natsort import natsorted

#library of BitTorrent simulator
#implements the core routines of the BitTorrent protocol

#variables to define the BitTorrent protocol behavior
NUM_TOP_PEERS = 4 #4 top peers is standard
REQUEST_BUFFER_SIZE = 10000 #request buffer size in reality can be extremely large, but in simulation too large can slow it down, but too small can cause congestion and result in peers never completing the download
RAREST_CHUNK_REQUEST_PERIOD = 5 #should be periodic but not too frequent that would make peers overly greedy
TOP_PEERS_REFRESH_PERIOD = 10 
OPTIMISTIC_UNCHOKE_PERIOD = 30 #the optimistic unchoke frequency being x3 as infrequent as the top peers reevaluation frequency is standard
LEAVE_WHEN_DONE = True #controls if peers churn after completion

#variables to define the simulation
HIGH_BANDWIDTH = 1000 #this is the absolute max bandwidth since it will correspond to a period of 1 time step
LOW_BANDWIDTH = 10
NUM_PEERS = 50
SIMULATION_TIME = 1500
NUM_CHUNKS = 100 #this is an abitrary amount but if too low, the simulator will be very coarse and not give much insight into the download behavior. Too large of a file will result in a slow simulation
DOWNLOAD_RATE_WINDOW = 10 #for calculation of the instantaneous download rate; smaller would yield very noisy but more accurate values, but larger would be more of a smoothed out value but with fewer data points


class Peer: #the core Peer class that represents a peer in the Torrent
    def __init__(self, IPAddress, bandwidth, peers, tracker, acquiredChunks):
        self.IPAddress = IPAddress #a peer should know its own public IP
        self.bandwidth = bandwidth #determined upon object creation, can be random just like real-life
        self.peers = peers #should have some information on all the hosts that exist in this simulated world
        self.tracker = tracker #should have meta data on the torrent, what the file is composed of, and the peers that are participating
        self.acquiredChunks = acquiredChunks #track the chunks it accumulates over time
        self.torrentSourceChunks = None #to store a reference of what a complete source file should look like
        self.receiveBuffer = [] #buffer as an inbox for all incoming chunks from other peers
        self.requestBuffer = [] #buffer as an inbox for all requests from other peers for chunks it has
        self.missingChunks = None #track what chunks are left to download
        self.downloadBandwidths = {} #track the rates at which other peers send chunks; useful for determining the top peers that deserve to be reciprocated
        self.topPeers = [] #track who are the top 4 peers
        self.currentlyRequestedChunk = None #track which chunks are currently being requested from other peers; this is to prevent the peer from over sending requests that can congest the Torrent
        self.timeJoinTracker = 0 #track at what time the peer joins the tracker
        self.numAcquiredChunksBefore = 0 #for download rate calculation later
        self.timeAcquiredChunksBefore = 0 #for download rate calculation later
        self.trackerPeerCount = 0 #for the peer to detect when peers come and go from the tracker

    def joinTracker(self, t): #routine for a peer to join a Torrent tracker
        self.tracker[1].append(self.IPAddress) #add IP to the tracker's list for other peers to see and lookup
        self.torrentSourceChunks = self.tracker[0] #get a copy of what the complete source file would compose of
        self.updateMissingChunks() #use the complete reference to decide which chunks we are missing
        self.timeJoinTracker = t #track at what time did we join the tracker
    
    def leaveTracker(self): #routine for a peer to leave a Torrent tracker
        self.tracker[1].remove(self.IPAddress) #leaving a tracker simply means removing one's IP address from the tracker's list so other peers can not look you up and request chunks

    def updateMissingChunks(self):
        self.missingChunks = list(set(self.torrentSourceChunks).difference(self.acquiredChunks))

    def refreshTopPeers(self): #a routine for a peer to reevaluate the top peers that send it chunks at the highest rates
        if len(self.downloadBandwidths) >= NUM_TOP_PEERS: #check if we have enough download information from peers to even select a top 4
            sortedDownloadBandwidths = dict(sorted(self.downloadBandwidths.items(), key=lambda item: item[1])) #sort the download bandwidths from smallest to largest
            descendingPeerRankings = list(reversed(sortedDownloadBandwidths.keys())) #get the corresponding peer IPs of the sorted bandwidths, and reverse the order
            self.topPeers = descendingPeerRankings[:NUM_TOP_PEERS] #the top 4 peers will be the first 4 peers of this list
        else: #if we still have not exchanged with at least 4 peers, we can not decide on the top 4 peers just yet
            self.topPeers = [] #so the top 4 peers do not exist
        self.downloadBandwidths = {} #clear out the download bandwidth tracker so the next time we reevaluate the top peers, it will not be neccessarily the same ones, and give others a chance to "show off" their contributions

    def optimisticallyUnchokePeer(self): #a routine for a peer to give a chance to a peer with lower download bandwidth, possibly a free rider
        if len(self.topPeers) > 0: #we only unchoke a peer if we already have a top 4 peers list going
            notTopPeers = list(set(self.tracker[1]).difference(self.topPeers)) #get the peers that are not in the top 4
            notTopPeersValid = [] #track the not top peers that have a request already in the buffer because there's no point unchoking a random peer who is not requesting chunks
            for notTopPeer in notTopPeers:
                for request in self.requestBuffer: #check if the not top peer has a request sitting in the buffer
                    if request[0] == notTopPeer and notTopPeer not in notTopPeersValid: 
                        notTopPeersValid.append(notTopPeer) #if the not top peer has a request sitting in the buffer, move it to the next stage of selection
            notTopPeers = notTopPeersValid
            if len(notTopPeers) == 0: #if there are no other requesting peers that are not in the top 4, we don't have to do any unchoking
                return 0
            randomPeerIndex = random.randint(0, len(notTopPeers) - 1) #randomly pick a not top peer
            randomlyPickedPeer = notTopPeers[randomPeerIndex] #randomly pick a not top peer
            topPeerRandomReplaceIndex = random.randint(0, NUM_TOP_PEERS - 1) #randomly pick a slot in the top 4 to replace with this peer
            self.topPeers[topPeerRandomReplaceIndex] = randomlyPickedPeer #replace a top 4 peer with this randomly unchoked one
            
    def getRarestChunkType(self): #function to ascertain the rarest chunks - the most desirable - in a Torrent
        chunksHistogram = {} #histogram to count the chunks to later determine rarity
        for trackerPeerID in self.tracker[1]: #iterate through all peers in a chunk
            if trackerPeerID != self.IPAddress:
                theirAcquiredChunks = self.peers[trackerPeerID].acquiredChunks #get the chunks the peer currently has
                for chunk in theirAcquiredChunks:
                    if chunk in self.missingChunks: #only count the chunk if it is a chunk we want
                        if chunk not in chunksHistogram: #add the count to the respective bin of the histogram
                            chunksHistogram[chunk] = 1
                        else:
                            chunksHistogram[chunk] = chunksHistogram[chunk] + 1

        chunksHistogram = dict(sorted(chunksHistogram.items(), key=lambda item: item[1])) #sort the chunks by chunk count, smallest to largest
        chunksSorted = list(chunksHistogram.keys()) #get the list of chunks, fewest count first
        return chunksSorted

    def requestRarestChunkFromPeers(self): #routine to periodically request the rarest chunks first from peers in the Torrent, the key to P2P architecture
        if self.currentlyRequestedChunk != None and not len(self.tracker[1]) != self.trackerPeerCount:
            #if either 1. the current chunks requested have not been fulfilled and 2. tracker peers have not changed
            #we do not need to do a rarest chunk request
            #this will prevent peers from over requesting, causing congestion
            for currentlyRequestedChunk in self.currentlyRequestedChunk:
                if currentlyRequestedChunk not in self.acquiredChunks:
                    return 0
        if len(self.missingChunks) > 0: #we only request chunks if we still have missing chunks
            rarestChunks = (self.getRarestChunkType())[:NUM_TOP_PEERS] #get the top 4 rarest chunks in the Torrent that are missing; we can control the amount of rare chunks considered to modulate the greediness of a peer; it may want to request more rare chunks in one shot but this will congest the Torrent
            self.currentlyRequestedChunk = rarestChunks #track the chunks that are about to be requested from others
            #a peer will only request new chunks only if its previous requests are fulfilled
            #essentially, a couple chunks at a time and request as needed!
            for rarestChunk in rarestChunks:
                chunkRequest = (self.IPAddress, rarestChunk) #construct the request packet (tuple) that is to be sent to the request buffer of others
                for trackerPeerID in self.tracker[1]: #iterate through all peers in the tracker so we can send the request to them
                    if trackerPeerID != self.IPAddress: #not requesting from ourselves
                        if chunkRequest not in self.peers[trackerPeerID].requestBuffer: #if the request already exists in a peer's inbox, no need to duplicate it, they will get to it eventually.... 
                            if rarestChunk in self.peers[trackerPeerID].acquiredChunks: #check if the other peer has the rare chunk
                                if len(self.peers[trackerPeerID].requestBuffer) < REQUEST_BUFFER_SIZE: #check if their request inbox is not full
                                    self.peers[trackerPeerID].requestBuffer.append(chunkRequest) #put the request in their request inbox
        self.trackerPeerCount = len(self.tracker[1]) #keep track of the peers in the tracker; if it changes, we need to send out new requests incase the peer that has left had our only request

    def processReceiveBuffer(self): #routine for a peer to receive chunks from others and update which chunks it is still missing
        for packet in self.receiveBuffer:
            self.downloadBandwidths[packet[0]] = packet[1] #track the sending peer's download bandwidth so we can consider it later in the top 4 evaluation
            if packet[2] in self.missingChunks: #if the sent chunk is a missing chunk, then great!
                chunkRequest = (self.IPAddress, packet[2]) #we must remove any requests of this now received chunk from others' inboxes so they don't pointlessly send it again
                for trackerPeerID in self.tracker[1]:
                        if trackerPeerID != self.IPAddress:
                            if chunkRequest in self.peers[trackerPeerID].requestBuffer: #check if the now-fulfilled request exists
                                self.peers[trackerPeerID].requestBuffer.remove(chunkRequest) #remove it
                                
                self.missingChunks.remove(packet[2]) #remove that chunk from the missing chunks list
                self.acquiredChunks.append(packet[2]) #add the chunk to the list of chunks we now have
        self.receiveBuffer = [] #empty out the receive buffer to later receive new chunks

    def sendChunkToPeer(self, chunk, bandwidth, peerIP): #send a chunk to a peer IP at a specified bandwidth
        chunkPacket = (self.IPAddress, bandwidth, chunk) #construct the datagram format as a 3-tuple
        self.peers[peerIP].receiveBuffer.append(chunkPacket) #put this datagram in the peer's inbox

    def sendChunksToTopPeers(self, t): #send chunks to peers that are requesting, but prioritize the top 4 peers
        requestCount = len(self.requestBuffer)
        if requestCount > 0: #we only need to send chunks if we have requests
            random.shuffle(self.requestBuffer) #shuffle the order of the request buffer if we are not basing off top 4
            #this is a caveat in the round-robin schedule; it triggers routines in peers in the order of their index within a time step
            #in other words, although it is a single time step, the routines are not actually happening in paralell but rather serially
            #thus, peer indexes lower will get to request before higher indexes, thus their requests may show up in inboxes before others perpetually
            #drowning out the higher index peers unfairly
            #to solve this problem, we shuffle the buffer

            sendBandwidth = int(self.bandwidth / NUM_TOP_PEERS) #our effective send bandwidth is split amongst the top peers
            if requestCount >= NUM_TOP_PEERS: #if there are more than 4 requests, we expect to only send to 4 peers, where we split the bandwidth equally
                sendBandwidth = int(self.bandwidth / NUM_TOP_PEERS) 
            else: #otherwise, we will send fewer than 4 times and thus must calculate the split bandwidth
                sendBandwidth = int(self.bandwidth / requestCount)

            if t % int((1 / sendBandwidth) * 1000) == 0: #we first convert the bandwidth to a period interval, then check if the peer is supposed to send chunks at a time step
                #the modulo operator effectively filters out routines based on an interval and mimics the periodicity of sending you would see for varying upload bandwidths
                peersSentTo = [] #track which peers have already had a chunk sent out to so we don't repeatedly send chunks to only one peer unfairly
                sendCount = 0
                remainingRequests = self.requestBuffer.copy()
                for request in self.requestBuffer: #iterate through the requests
                    if (request[0] in self.topPeers or len(self.topPeers) == 0): #check if the request is from a top 4 peer
                        #otherwise, if we don't have top peers, just go in order of the request buffer
                        if request[0] not in peersSentTo:
                            peersSentTo.append(request[0])
                            self.sendChunkToPeer(request[1], sendBandwidth, request[0]) #send the chunk to the peer
                            remainingRequests.remove(request) #remove the request
                            sendCount = sendCount + 1
                            if sendCount == NUM_TOP_PEERS: #stop sending if we have reached the send limit of 4 chunks
                                break
                self.requestBuffer = remainingRequests.copy() #update the request buffer after fufilling some requests
    
    def getDownloadPercentage(self): #function to query a peer's progress on downloading the file
        if self.torrentSourceChunks == None:
            return 0
        sourceFileChunkCount = len(self.torrentSourceChunks)
        acquiredChunkCount = len(self.acquiredChunks)
        if sourceFileChunkCount > 0:
            percentage = (acquiredChunkCount / sourceFileChunkCount) * 100 #the progress is the ratio of chunks the peer has over the total chunks of the source file
            return percentage
        
    def getDownloadRate(self, t): #function to calculate the instantaneous download rate over a window
        if self.timeAcquiredChunksBefore == 0 or self.numAcquiredChunksBefore == 0:
            rate = 0
        else:
            rate = (len(self.acquiredChunks) - self.numAcquiredChunksBefore) / ((t - self.timeAcquiredChunksBefore))
        self.timeAcquiredChunksBefore = t
        self.numAcquiredChunksBefore = len(self.acquiredChunks)
        return rate

    def print(self): #debug print function
        print("--------")
        print("IP: " + str(self.IPAddress))
        print("Bandwidth: " + str(self.bandwidth))
        print("Acquired chunks: " + str(natsorted(self.acquiredChunks)))
        print("Receive buffer: " + str(self.receiveBuffer))
        print("Request buffer: " + str(self.requestBuffer))
        print("Missing chunks: " + str(natsorted(self.missingChunks)))
        print("Top " + str(NUM_TOP_PEERS) +  " peers: " + str(natsorted(self.topPeers)))
        print("Download bandwidths: " + str(self.downloadBandwidths))
        print("Upload bandwidths: " + str(self.uploadBandwidths))
        print("Rarest chunk requested: " + str(self.currentlyRequestedChunk))
        print("--------")

