class Neuron:
    def __init__(self, l_id, id, neuron_per_pe, PE_num):
        self.id = id
        self.layerId = l_id
        self.dests = []
        self.neuron_per_pe = neuron_per_pe
        self.PE_limit = PE_num

    def PE_num(self):
        return int(self.id / self.neuron_per_pe)
