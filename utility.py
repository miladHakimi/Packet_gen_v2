from PE import PE
def print_packets(packets, id):
    print("############################################ layer id = " + str(id) + "##########################################")
    for i in packets:
        for j in i:
            print(j)

def PE_gen(LAYER_filters, PE_PER_LEAF, LEAF_COUNT):
    PEs = []
    for i in range(LAYER_filters):
        leaf_num = int(i/(PE_PER_LEAF-1))
        pe_index = i % (PE_PER_LEAF-1)
        pe_id = (leaf_num*PE_PER_LEAF+pe_index) % (PE_PER_LEAF*LEAF_COUNT)
        PEs.append(PE(pe_id, "PE", 0))
    return PEs

def mem_gen(LAYER_MEMS, LEAF_COUNT):
    mems = []
    for i in range(LAYER_MEMS):
        mems.append(PE(i%LEAF_COUNT, "MEM"))

    return mems

def assign_dests(PEs, mems, LEAF_COUNT):
    for i in PEs:
        for j in mems:
            j.dests.append(i)
            if (int(i.id/LEAF_COUNT))%LEAF_COUNT == j.id:
                i.iterations += 1
        try:
            i.dests.append(mems[(int(i.id/LEAF_COUNT))%LEAF_COUNT])
        except  IndexError:
            pass