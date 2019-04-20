from PE import PE
# global info

PE_PER_LEAF = 8
LEAF_COUNT = 8
INJECTION_RATE = 50 
LAYER_MEMS = 8
LAYER_filters = 96

IMG_EDGE = 10
FILTER_EDGE = 3

PEs = []
mems = []

for i in range(LAYER_filters):
    leaf_num = i/(PE_PER_LEAF-1)
    pe_index = i % (PE_PER_LEAF-1)
    pe_id = (leaf_num*PE_PER_LEAF+pe_index) % (PE_PER_LEAF*LEAF_COUNT)
    PEs.append(PE(pe_id))

for i in range(LAYER_MEMS):
    mems.append(PE(i%LEAF_COUNT, "MEM"))

for i in PEs:
    for j in mems:
        j.dests.append(i)

    i.dests.append(mems[(i.id/LEAF_COUNT)%LEAF_COUNT])

# generate packets
packets = []

for i in mems:
    packets.append(i.create_packets(INJECTION_RATE, LEAF_COUNT, PE_PER_LEAF, IMG_EDGE-FILTER_EDGE+1))

for i in PEs:
    packets.append(i.create_packets(INJECTION_RATE, LEAF_COUNT, PE_PER_LEAF, IMG_EDGE-FILTER_EDGE+1))
