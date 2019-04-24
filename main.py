from PE import PE
from ConvLayer import ConvLayer
from utility import *

# global info
PE_PER_LEAF = 8
LEAF_COUNT = 8
INJECTION_RATE = 50 
first_layer_mems = 1

conv_layers_count = 2

# (filter_count, filter_size)
layer_desc = [(20, 5), (50, 5), (10, 3)]

PEs = PE_gen(layer_desc[0][0], PE_PER_LEAF, LEAF_COUNT)
mems = mem_gen(first_layer_mems, LEAF_COUNT)
assign_dests(PEs, mems, LEAF_COUNT)

# generate layers
layers = []
layers.append(ConvLayer(1, layer_desc[0][0], PEs, mems, PE_PER_LEAF, LEAF_COUNT, layer_desc[0][1], 100))
packets = layers[0].generate_packets(INJECTION_RATE, 0)
print_packets(packets, 0)

for i in range(conv_layers_count-1):
        mem_count = layers[i].output_count
        filter_count = layer_desc[i+1][0]

        PEs = PE_gen(filter_count, PE_PER_LEAF, LEAF_COUNT)
        mems = mem_gen(mem_count, LEAF_COUNT)

        assign_dests(PEs, mems, LEAF_COUNT)
        
        layers.append(ConvLayer(mem_count, filter_count, PEs, mems, PE_PER_LEAF, LEAF_COUNT, layer_desc[i+1][1],layers[i].out_img_size))
        print_packets(layers[-1].generate_packets(INJECTION_RATE, layers[i].finish_time), i+1)