packet_id = 0

class Packet:
    def __init__(self, time, dests, src):
        global packet_id
        self.src = src
        self.id = packet_id
        self.time = time
        self.dests = dests
        
        packet_id += 1

    def __str__(self):
        ans = ""
        for i in self.dests:
            ans += self.src + "     " + i.type + "_"+ str(i.id) + "      " + str(self.time) + "      " + str(self.id) + "\n"
        
        return ans