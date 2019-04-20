from Layer import Layer
from PE import PE

class ConvLayer(Layer):
    def __init__(self, input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count, output_size):
        super().__init__(input_count, output_count, PEs, MEMs)
        self.output_size = output_size
        
    def generate_packets(self, INJECTION_RATE):
        packets = []
        for i in range(self.input_count):
            packets.append(self.MEMs[i%self.leaf_count].create_packets(INJECTION_RATE, self.leaf_count, self.pe_per_leaf, self.output_size))

        for i in self.output_count:
            packets.append(self.PEs[i%len(self.PEs)].create_packets(INJECTION_RATE, self.leaf_count, self.pe_per_leaf, self.output_size))

