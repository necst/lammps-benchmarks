import pandas as pd 
import os 
import sys

# modify to change the experiments to group together
experiments = ["rhodo", "rhodo-single", "rhodo-double"]
mpi_nproc = [1, 2, 4, 8, 16, 32, 64]
nk_atoms = [32, 256, 864, 2048]

def get_file_name(bench, nproc, nk_atoms):
    name = "in." + bench 
    if nk_atoms > 32 and ((bench == "chain") or (bench == "rhodo")):
        name += ".scaled.timer"
    else:
        name += ".timer"
    
    name += "_" + str(nproc) + "n_1ont_" + str(nk_atoms) + "k_aps.csv"
    return name

mpi_funcs = set() # MPI functions
mpi_data = []

files = os.listdir(os.getcwd())
filename = sys.argv[1]

for fname in files:
    if fname.endswith(".csv") and fname.startswith("in."):
        try:
            file = open(fname, "r")
            in_mpi_calls = False
            in_total_time = False
            params = fname.replace(".scaled","").split('_')
            if params[1].endswith('-double'):
                params[0] += '-double'
            elif params[1].endswith('-single'):
                params[0] += '-single'
            bench = params[0]
            exp_size = int(params[len(params)-2][:-1])
            exp_proc = int(params[len(params)-4][:-1])
            if (bench[3:] not in experiments):
                print(bench[3:] + " not found!")
                continue
            if (exp_size not in nk_atoms):
                print(exp_size + " not found!")
                continue
            if (exp_proc not in mpi_nproc):
                print(exp_proc + " not found!")
                continue
            print(params)
            times_dict = {"Benchmark" : bench} # mapping func : time%
            times_dict['Size'] = int(params[len(params)-2][:-1])
            times_dict['Processes'] = int(params[len(params)-4][:-1])

            for line in file:
                if line.find("Function summary for all Ranks") >= 0:
                    in_mpi_calls = True
                if line[0:7] == "| TOTAL":
                    in_mpi_calls = False
                if in_total_time  and (line[0:7] == "| TOTAL"):
                    in_total_time = False
                    tokens = line.split(";")
                    tokens = [x.strip() for x in tokens]
                    times_dict['MPI_Time'] = float(tokens[2])
                    times_dict['MPI_(%)'] = float(tokens[3])
                    if 'MPI_Time' not in mpi_funcs:
                        mpi_funcs.add('MPI_Time')
                    if 'MPI_(%)' not in mpi_funcs:
                        mpi_funcs.add('MPI_(%)')
                if line.find("| MPI Time per Rank for all Ranks") >= 0:
                    in_total_time = True
                if in_mpi_calls:
                    if line.find("MPI_") >= 0:
                        tokens = line.split(";")
                        tokens = [x.strip() for x in tokens]
                        if tokens[0] not in mpi_funcs:
                            mpi_funcs.add(tokens[0])
                        times_dict[tokens[0]] = float(tokens[2])
            mpi_data.append(times_dict)
        except IOError:
            print("File not found: " + fname)

for el in mpi_data:
    for func in mpi_funcs:
        if func not in el.keys():
            el[func] = 0.0

header = ["Benchmark"] + list(mpi_funcs)
df = pd.DataFrame(columns=header)

for row in mpi_data:
    df = df.append(row, ignore_index=True)
print(df)
col = df['MPI_Time']
df.drop(labels=['MPI_Time'], axis=1,inplace = True)
df.insert(1, 'MPI_Time', col)
col = df['MPI_(%)']
df.drop(labels=['MPI_(%)'], axis=1,inplace = True)
df.insert(1, 'MPI_(%)', col)
df = df.sort_values(['Benchmark','Size','Processes'])
df.groupby(['Size','Processes'])
print(df)
df.to_csv(filename + ".csv", index=False)
df.to_excel(filename + ".xlsx", index=False)
            
