from PE import PE
from ConvLayer import ConvLayer
from utility import *
from FullyConnected import FullyConnected

# global info
PE_PER_LEAF = 8
LEAF_COUNT = 8
INJECTION_RATE = 50 
first_layer_mems = 1
PE_COUNT = (PE_PER_LEAF-1)*LEAF_COUNT
input_size = 27
# (filter_count, filter_size)
# Alex_net
# layer_desc = [(20, 5), (50, 5), (10, 3)]
# mobile_net
layer_desc = [(32, 3), (32,3), (64, 1), (64, 3), (128, 1), (128, 3), (128, 1), (128, 3), (256, 1), (256, 3), (256, 1), (256, 3), 
        (512, 1), (512, 3), (512, 1), (512, 3), (512, 1), (512, 3), (512, 1), (512, 3), (512, 1), (512, 3), (512, 1), (512, 3), 
        (1024, 1), (1024, 3), (1024, 1)]

# fully_connected_settings = [500, 10]
# resnet
# layer_desc = [(64, 7), (256, 1), (64, 1), (64, 3), (256, 1), (64, 1), (64, 3), (256, 1),
#         (64, 1), (64, 3), (256, 1), (512, 1), (128, 1), (128, 3), (512, 1), (128, 1), (128, 3),
#         (512, 1), (128, 1), (128, 3), (512, 1), (128, 1), (128, 3)
#         ]
fully_connected_settings = [1000, 1]

PEs = PE_gen(layer_desc[0][0], PE_PER_LEAF, LEAF_COUNT)
mems = mem_gen(first_layer_mems, LEAF_COUNT)
assign_dests(PEs, mems, LEAF_COUNT)

# generate layers
layers = []
layers.append(ConvLayer(1, layer_desc[0][0], PEs, mems, PE_PER_LEAF, LEAF_COUNT, layer_desc[0][1], 20))
packets = layers[0].generate_packets(INJECTION_RATE, 0)
print_packets(packets, 0)

for i in range(len(layer_desc)-1):
        mem_count = layers[i].output_count
        filter_count = layer_desc[i+1][0]

        PEs = PE_gen(filter_count, PE_PER_LEAF, LEAF_COUNT)
        mems = mem_gen(mem_count, LEAF_COUNT)

        assign_dests(PEs, mems, LEAF_COUNT)
        
        layers.append(ConvLayer(mem_count, filter_count, PEs, mems, PE_PER_LEAF, LEAF_COUNT, layer_desc[i+1][1],layers[i].out_img_size))
        print_packets(layers[-1].generate_packets(INJECTION_RATE, layers[i].finish_time), i+1)
     
        print(len(PEs))
packets = fc_gen(PE_PER_LEAF, LEAF_COUNT, layers, fully_connected_settings, INJECTION_RATE, mems, PE_COUNT )

print_packets(packets, len(layers), False)
