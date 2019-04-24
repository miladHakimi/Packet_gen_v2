from Layer import Layer
from PE import PE

class ConvLayer(Layer):
    def __init__(self, input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count, filter_size, img_size):
        super().__init__(input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count)
        self.filter_size = filter_size
        self.input_image_size = img_size
        
    def generate_packets(self, INJECTION_RATE):
        packets = []
        for i in range(self.input_count):
            packets.append(self.MEMs[i%self.leaf_count].create_packets(INJECTION_RATE, self.leaf_count, self.pe_per_leaf, self.input_image_size-self.filter_size+1))

        for i in range(self.output_count):
            packets.append(self.PEs[i%(self.leaf_count*(self.pe_per_leaf))].create_packets(INJECTION_RATE, self.leaf_count, self.pe_per_leaf, self.input_image_size-self.filter_size+1))

        return packets
