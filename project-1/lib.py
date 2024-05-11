import random
from natsort import natsorted

NUM_TOP_PEERS = 4
REQUEST_BUFFER_SIZE = 500
HIGH_BANDWIDTH = 1000
LOW_BANDWIDTH = 20

class Peer:
    def __init__(self, IPAddress, bandwidth, peers, tracker, acquiredChunks):
        self.IPAddress = IPAddress
        self.bandwidth = bandwidth
        self.peers = peers
        self.tracker = tracker
        self.acquiredChunks = acquiredChunks 
        self.torrentSourceChunks = None
        self.receiveBuffer = []
        self.requestBuffer = []
        self.missingChunks = None
        self.downloadBandwidths = {}
        self.uploadBandwidths = {}
        self.topPeers = []
        self.currentlyRequestedChunk = None

    def refreshTopPeers(self):
        if len(self.downloadBandwidths) >= NUM_TOP_PEERS:
            sortedDownloadBandwidths = dict(sorted(self.downloadBandwidths.items(), key=lambda item: item[1]))
            #print(sortedDownloadBandwidths)
            descendingPeerRankings = list(reversed(sortedDownloadBandwidths.keys()))
            #print(descendingPeerRankings)
            #print(descendingPeerRankings[:4])
            self.topPeers = descendingPeerRankings[:NUM_TOP_PEERS]
        else:
            self.topPeers = []
        self.downloadBandwidths = {}


    def clearRequestBuffer(self): 
        self.requestBuffer = []

    def optimisticallyUnchokePeer(self):
        if len(self.topPeers) > 0:
            notTopPeers = list(set(self.tracker[1]).difference(self.topPeers))
            randomPeerIndex = random.randint(0, len(notTopPeers) - 1)
            randomlyPickedPeer = notTopPeers[randomPeerIndex]
            topPeerRandomReplaceIndex = random.randint(0, NUM_TOP_PEERS - 1)
            self.topPeers[topPeerRandomReplaceIndex] = randomlyPickedPeer
            
    def getRarestChunkType(self):
        chunksHistogram = {}
        for trackerPeerID in self.tracker[1]:
            if trackerPeerID != self.IPAddress:
                theirAcquiredChunks = self.peers[trackerPeerID].acquiredChunks
                for chunk in theirAcquiredChunks:
                    if chunk in self.missingChunks:
                        if chunk not in chunksHistogram:
                            chunksHistogram[chunk] = 1
                        else:
                            chunksHistogram[chunk] = chunksHistogram[chunk] + 1

        chunksHistogram = dict(sorted(chunksHistogram.items(), key=lambda item: item[1]))
        chunksSorted = list(chunksHistogram.keys())
        return chunksSorted

    def broadcastBandwidth(self):
        for peerID in self.top4Peers:
            self.peers[peerID].downloadBandwidths[self.IPAddress] = self.bandwidth / 4
            self.uploadBandwidths[peerID] = self.bandwidth / 4

    def joinTracker(self):
        self.tracker[1].append(self.IPAddress)
        self.torrentSourceChunks = self.tracker[0]
        self.updateMissingChunks()
    
    def leaveTracker(self):
        self.tracker[1].remove(self.IPAddress)

    def updateMissingChunks(self):
        self.missingChunks = list(set(self.torrentSourceChunks).difference(self.acquiredChunks))

    def sendRandomHellos(self):
        for peerID in self.tracker[1]:
            if peerID != self.IPAddress:
                self.peers[peerID].receiveBuffer.append("hello from " + str(self.IPAddress))

    def requestRarestChunkFromPeers(self):
            if self.currentlyRequestedChunk != None:
                for currentlyRequestedChunk in self.currentlyRequestedChunk:
                    if currentlyRequestedChunk not in self.acquiredChunks:
                        return 0
            if len(self.missingChunks) > 0:
                rarestChunks = (self.getRarestChunkType())[:10]
                self.currentlyRequestedChunk = rarestChunks
                for rarestChunk in rarestChunks:
                    chunkRequest = (self.IPAddress, rarestChunk)
                    for trackerPeerID in self.tracker[1]:
                        if trackerPeerID != self.IPAddress:
                            if chunkRequest not in self.peers[trackerPeerID].requestBuffer:
                                if rarestChunk in self.peers[trackerPeerID].acquiredChunks:
                                    if len(self.peers[trackerPeerID].requestBuffer) < REQUEST_BUFFER_SIZE:
                                        self.peers[trackerPeerID].requestBuffer.append(chunkRequest)
                                        #break

    

    def sendChunkToPeer(self, chunk, bandwidth, peerIP):
        chunkPacket = (self.IPAddress, bandwidth, chunk)
        self.peers[peerIP].receiveBuffer.append(chunkPacket)

    def processReceiveBuffer(self):
        #self.downloadBandwidths = {}
        for packet in self.receiveBuffer:
            self.downloadBandwidths[packet[0]] = packet[1]
            if packet[2] in self.missingChunks:

                chunkRequest = (self.IPAddress, packet[2])
                for trackerPeerID in self.tracker[1]:
                        if trackerPeerID != self.IPAddress:
                            if chunkRequest in self.peers[trackerPeerID].requestBuffer:
                                self.peers[trackerPeerID].requestBuffer.remove(chunkRequest)
                                
                self.missingChunks.remove(packet[2])
                self.acquiredChunks.append(packet[2])
        self.receiveBuffer = []

    def sendChunksToTopPeers(self, t):
        requestCount = len(self.requestBuffer)
        if requestCount > 0:

            random.shuffle(self.requestBuffer)

            sendBandwidth = int(self.bandwidth / NUM_TOP_PEERS) 

            if requestCount >= NUM_TOP_PEERS:
                sendBandwidth = int(self.bandwidth / NUM_TOP_PEERS) 
            else:
                sendBandwidth = int(self.bandwidth / requestCount)


            if t % int((1 / sendBandwidth) * 1000) == 0:
                peersSentTo = []
                sendCount = 0
                remainingRequests = self.requestBuffer.copy()
                #random.shuffle(self.requestBuffer)
                for request in self.requestBuffer:
                    if (request[0] in self.topPeers or len(self.topPeers) == 0):
                        if request[0] not in peersSentTo:
                            peersSentTo.append(request[0])
                            self.sendChunkToPeer(request[1], sendBandwidth, request[0])
                            remainingRequests.remove(request)
                            sendCount = sendCount + 1
                            if sendCount == NUM_TOP_PEERS:
                                break
                self.requestBuffer = remainingRequests.copy()
    
    def getDownloadPercentage(self):
        sourceFileChunkCount = len(self.torrentSourceChunks)
        acquiredChunkCount = len(self.acquiredChunks)

        if sourceFileChunkCount > 0:
            percentage = (acquiredChunkCount / sourceFileChunkCount) * 100
            return percentage

    def print(self):
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

