import random
from Packet import Packet
import math
import numpy as np

class PE:
	def __init__(self, id, pe_per_leaf, t="PE", iterations=1, layer_type="conv"):
		self.childs = []
		self.id = id
		self.dests = []
		self.type = t
		self.iterations = iterations
		self.neurons = []
		self.Pe_per_leaf = pe_per_leaf
		self.packets = []

	def create_packets(self, injection_rate, leaf_count, PE_per_leaf, row_number, start_time):
		packets = []
		i = 0
		for p in range(self.iterations):
			for i in range(row_number):
				dests = []
				for j in self.dests:
					if j.type != "PE":
						dests.append(int(self.id/PE_per_leaf)+PE_per_leaf-1)
					else:
						dests.append(j.id)
				dests = self.multicast_detect(dests)
				rand_time = random.randint(i*injection_rate, (i+1)*injection_rate) + start_time
				for j in dests:
					packets.append(Packet(rand_time, j, self.type + '_' +str(self.id)))

		self.packets = packets
		return packets

	def create_packet_fc(self, inj_rate, time_limit, start_time, pe_per_leaf):
		if len(self.dests) == 0:
			return None
		packets = []
		iterations = math.ceil(time_limit * inj_rate)
		r = int(1/(inj_rate*1.0))

		# dests = self.dest_gen(pe_per_leaf)
		dests = self.multicast_detect(self.dests)
		for i in range(iterations):
			t = random.randint(1 ,r)
			t += i*r + start_time
			for dest in dests:
				p = Packet(t, dest, self.type + "_" + str(self.id))
				packets.append(p)

		self.packets = packets
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

	def write_in_file(self):
		packets = []
		
		if len(self.packets) > 0:
			packets = self.packets

		for i in self.childs:
			if len(i.packets) > 0:
				packets += i.packets
		
		p = sorted(packets, key=lambda x: x.time, reverse=False)
		PEID, leafID = self.extract_IDs()

		f = open("input_0_" + str(leafID) + "_" + str(PEID) + ".txt", "w+")
		
		writeData = self.generate_write_data(p)
		
		f.write(writeData)
		f.close()
	
	def extract_IDs(self):
		leafID = int(self.id/self.Pe_per_leaf)
		PEID = self.id%(self.Pe_per_leaf-1)
		
		if self.type == "MEM":
			PEID = self.Pe_per_leaf-1
			leafID = self.id

		return PEID, leafID
	def generate_write_data(self, packets):
		writeData = ""
		for i in packets:
			destLeaf = "0000000000000000"
			destPE = "0000000000000000"
			for j in i.dests:
				LeafIndex = int(j/self.Pe_per_leaf)
				list1 = list(destLeaf)
				list1[15-LeafIndex] = '1'
				destLeaf = ''.join(list1)
			for j in i.dests:
				list1 = list(destPE)
				list1[15- j%self.Pe_per_leaf] = '1'
				destPE = ''.join(list1)
			writeData +=  destLeaf + destPE + "0" + "       " + str(i.time) + "	" + str(i.id)+"\n"
		
		return writeData

	def multicast_detect(self, dests):
		dest_map = {}
		leaf_map = {}
		pe_map = {}
		for i in dests:
			pe_id = i % self.Pe_per_leaf
			leaf_id = int(i / self.Pe_per_leaf)%8
			dest_map[(leaf_id, pe_id)] = i

			if leaf_id in leaf_map:
				leaf_map[leaf_id].append(pe_id)
			else:
				leaf_map[leaf_id] = [pe_id]
		
		ignore_list = []
		for i in leaf_map:
			if i not in ignore_list:
				for j in leaf_map:
					if j not in ignore_list:
						if self.check_equal(leaf_map[i], leaf_map[j]):
							new_dests = self.remake_dests(leaf_map[i], i, j, dest_map)
							pes = sorted(leaf_map[i])
							if self.to_string(pes) not in pe_map:
								pe_map[self.to_string(pes)] = new_dests
							else:
								pe_map[self.to_string(pes)]+= new_dests
							ignore_list.append(j)

	
		final_dests = []
		for i in pe_map:
			final_dests.append(pe_map[i])

		return final_dests
		
	def check_equal(self, map1, map2):
		for i in map1:
			if i not in map2:
				return False
		return True

	def remake_dests(self, map1, i, j, dest_map):
		dests = []
		for k in map1:
			dests.append(dest_map[(i, k)])
			if i != j:
				dests.append(dest_map[(j, k)])
		
		return dests

	def to_string(self, l1):
		s = [str(x) for x in l1]
		return int("".join(s))