from abc import abstractmethod

class Layer:
    def __init__(self, input_count, output_count, PEs, MEMs, pe_per_leaf, leaf_count):
        self.input_count = input_count
        self.output_count = output_count
        self.PEs = PEs
        self.MEMs = MEMs
        self.pe_per_leaf = pe_per_leaf
        self.leaf_count = leaf_count
    
    @abstractmethod
    def assign_inputs(self):
        pass
    
    @abstractmethod
    def generate_packets(self, INJECTION_RATE, start_time):
        pass    