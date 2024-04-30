class Peer:
    def __init__(self, name, IPAddress):
        self.name = name
        self.IPAddress = IPAddress

    def sendChunk(self, dest):
        chunk = "hello"
        return (chunk, dest)

    




peer1 = Peer("comp1", "123.3.3.2")
peer2 = Peer("comp2", "122.3.3.2")

print(peer1.sendChunk("122.3.3.2"))