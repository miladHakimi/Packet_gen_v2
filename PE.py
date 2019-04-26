import random
from Packet import Packet
import math


class PE:
	def __init__(self, id, t="PE", iterations=1):
		self.id = id
		self.dests = []
		self.type = t
		self.iterations = iterations
		self.neurons = []

	def create_packets(self, injection_rate, leaf_count, PE_per_leaf, row_number, start_time):
		packets = []
		i = 0
		for p in range(self.iterations):
			for i in range(row_number):
				rand_time = random.randint(i*injection_rate, (i+1)*injection_rate) + start_time
				packets.append(Packet(rand_time, self.dests, self.type + '_' +str(self.id)))
		return packets

	def create_packet_fc(self, inj_rate, time_limit, start_time, pe_per_leaf):
		if len(self.dests) == 0:
			return None
		packets = []
		iterations = math.ceil(time_limit * inj_rate)
		r = int(1/(inj_rate*1.0))

		dests = self.dest_gen(pe_per_leaf)

		for i in range(iterations):
			t = random.randint(1 ,r)
			t += i*r + start_time
			for dest in dests:
				p = Packet(t, dest, self.type + str(self.id))
				packets.append(p)

		return packets

	def dest_gen(self, pe_per_leaf):
		ans = []
		for dest in self.dests:
			p = []
			for i in range(pe_per_leaf):
				if int(dest/pe_per_leaf)*pe_per_leaf+i in self.dests:
					p.append(int(dest/pe_per_leaf)*pe_per_leaf+i)
			if p not in ans:
				ans.append(p)

		return ans
	
	def set_dests(self, n_per_p):
		self.dests = []
		for i in self.neurons:
			for j in i.dests:
				p = j.PE_num()
				if p not in self.dests and (p % n_per_p) is not self.id:
					self.dests.append(p)