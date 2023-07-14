import numpy as np

def merge_pulses(pulses :dict, name: str):
            coupling = {}
            done = []
            k = 0

            values = list(pulses.values())
            for i in range(len(values)):
                if i in done: continue
                v1 = values[i]

                for j in range(len(values)):
                    
                    if i == j: continue
                    
                    v2 = values[j]

                    # Matching the same levels of coupling
                    if v2[0] == v1[0]:
                        v1 = [v1[0], v1[1], np.add(v1[2], v2[2])]
                        values[i] = v1
                        done.append(j)

                coupling[name+str(k)] = v1
                done.append(i)
                k += 1

            return coupling