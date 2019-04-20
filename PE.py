import random
from Packet import Packet

class PE:
	def __init__(self, id, t="PE"):
		self.id = id
		self.dests = []
		self.type = t

	def create_packets(self, injection_rate, leaf_count, PE_per_leaf, row_number=1):
		packets = []
		for i in range(row_number):
			rand_time = random.randint(i*injection_rate, (i+1)*injection_rate)
			packets.append(Packet(rand_time, self.dests, self.type + '_' +str(self.id)))
		for i in packets:
			print(i)