from Layer import Layer
from Neuron import Neuron

class FullyConnected(Layer):
    def __init__(self, input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count, neuron_per_pe, first_index, PE_count):
        super().__init__(input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count)
        self.id = 0
        self.neurons = []
        self.neuron_per_pe = neuron_per_pe
        self.next_layer = None
        self.firstIndex = first_index
        self.PE_count = PE_count
        self.neuron_gen()
        
    def neuron_gen(self):
        for i in range(self.output_count):
            self.neurons.append(Neuron(self.id, i + self.firstIndex, self.neuron_per_pe, self.PE_count))
    
    def set_next_layer(self, layer):
        self.nextLayer = layer
        for i in self.neurons:
            i.dests = layer.neurons

    def map_neurons_to_pe(self, PEs, lastIndex=0):
        for i in self.neurons:
            try:
                PEs[i.PE_num()- lastIndex].neurons.append(i)
            except IndexError:
                print("problem in number of PEs")