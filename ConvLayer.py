from Layer import Layer
from PE import PE

class ConvLayer(Layer):
    def __init__(self, fmap_count, filter_count, PEs, MEMs, pe_per_leaf, leaf_count, filter_size, img_size):
        super().__init__(fmap_count, filter_count, PEs, MEMs, pe_per_leaf, leaf_count)
        self.filter_size = filter_size
        self.input_image_size = img_size
        self.out_img_size = self.input_image_size-self.filter_size+1 if self.input_image_size-self.filter_size>self.filter_size else self.filter_size
        self.finish_time = 0
        
    def generate_packets(self, INJECTION_RATE, start_time):
        packets = []
        self.finish_time = INJECTION_RATE * self.out_img_size + start_time
        for i in range(self.input_count):
            mem = self.MEMs[i%self.leaf_count]
            packets.append(mem.create_packets(INJECTION_RATE,
             self.leaf_count, self.pe_per_leaf, self.out_img_size, start_time))

        for i in range(self.output_count):
            packets.append(self.PEs[i%(self.leaf_count*(self.pe_per_leaf))].create_packets(INJECTION_RATE, self.leaf_count, self.pe_per_leaf, self.out_img_size, start_time))

        return packets
