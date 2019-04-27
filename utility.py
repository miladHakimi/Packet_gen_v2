from PE import PE
from FullyConnected import FullyConnected


def print_packets(packets, id):
    print("############################################ layer id = " + str(id) + " ##########################################")
    for i in packets:
        if i is not None:
            for j in i:
                print(j)

def PE_gen(LAYER_filters, PE_PER_LEAF, LEAF_COUNT, PES):
    PEs = []
    for i in range(LAYER_filters):
        leaf_num = int(i/(PE_PER_LEAF-1))
        pe_index = i % (PE_PER_LEAF-1)
        pe_id = (leaf_num*PE_PER_LEAF+pe_index) % (PE_PER_LEAF*LEAF_COUNT)
        new_pe = PE(pe_id, PE_PER_LEAF, "PE", 0)
        if pe_id in PES:
                PES[pe_id].childs.append(new_pe)
        else:
                PES[pe_id] = new_pe

        PEs.append(new_pe)
    return PEs

def mem_gen(LAYER_MEMS, LEAF_COUNT, PE_PER_LEAF, MEMs):
    mems = []
    for i in range(LAYER_MEMS):
        new_mem = PE(i%LEAF_COUNT, PE_PER_LEAF, "MEM")
        if i%LEAF_COUNT in MEMs:
                MEMs[i%LEAF_COUNT].childs.append(new_mem)
        else:
                MEMs[i%LEAF_COUNT] = new_mem

        mems.append(new_mem)

    return mems

def assign_dests(PEs, mems, LEAF_COUNT):
    for i in PEs:
        for j in mems:
            j.dests.append(i)
            i.iterations += 1
            
        try:
            i.dests.append(mems[(int(i.id/LEAF_COUNT))%LEAF_COUNT])
        except IndexError:
            print("problem in assign dests")
    
def fc_gen(PE_PER_LEAF, LEAF_COUNT, layers, fully_connected_settings, INJECTION_RATE, mems, PE_COUNT, PES, MEMs ):
    m = 0
    max0 = 0
    max1 = 1

    if fully_connected_settings==[]:
        return None
        
    for i in range(len(fully_connected_settings)-1):
            if fully_connected_settings[i] + fully_connected_settings[i+1] > m:
                    max0 = fully_connected_settings[i]
                    max1 = fully_connected_settings[i+1]
                    m = fully_connected_settings[i] + fully_connected_settings[i+1]
            
    NEURON_PER_PE = int((max0 + max1) /(LEAF_COUNT*(PE_PER_LEAF-1)))+1
    Pes = PE_gen(56, PE_PER_LEAF, LEAF_COUNT, PES)
    
    fc0 = FullyConnected(layers[-1].output_count, max0, Pes, mems, PE_PER_LEAF, LEAF_COUNT, NEURON_PER_PE, 0, PE_COUNT)
    fc1 = FullyConnected(max0, max1, Pes, mems, PE_PER_LEAF, LEAF_COUNT, NEURON_PER_PE, fc0.neurons[-1].id+1, PE_COUNT)
    fc0.set_next_layer(fc1)
    fc0.map_neurons_to_pe(Pes)
    for i in Pes:
            i.set_dests(NEURON_PER_PE)
    packets = []
    for i in Pes:
            packets.append(i.create_packet_fc(1/(INJECTION_RATE*1.0), 1, layers[-1].finish_time, PE_PER_LEAF-1))
    
    return packets