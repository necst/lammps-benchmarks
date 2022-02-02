# This script defines custom parsers to extract performance metrics from raw output

import pandas as pd
import re
import os 

# Testing parser for hello toy benchmark
def hello_parser(runs_data, out_file, timestamp):
    try:
        outf = open(out_file, mode='r')
        data = outf.read()
        z = re.search(r'(\d+ GFLOPs)|(\d+\.\d+ GFLOPs)', str(data))
        perf = re.search(r'(\d)|(\d+\.\d)', z.group()).group()
        runs_data.loc[timestamp,'PERFORMANCE'] = perf
    finally:
        outf.close()

    return runs_data

# Testing parser for hpcg_cpu benchmark
def hpcg_cpu_parser(runs_data, out_file, timestamp, logs_dir):
    try:
        outf = open(out_file, mode='r')
        data = outf.read()
        z = re.search(r'of \d+\.\d+', str(data))
        perf = re.search(r'(\d+\.\d+)', z.group()).group()
        runs_data.loc[timestamp,'PERFORMANCE'] = perf
        
        # Rename and move additional log files
        cwd = os.getcwd()
        log_res = re.compile(r'hpcg\d+T\d+\.txt')
        log_run = re.compile(r'n\d+-\d+p-\d+t.*\.txt')
        for file in os.walk(cwd):
            if log_res.match(file):
                os.system('mv ' + file + ' ' + logs_dir + '/' + timestamp + '_residual.txt')
            if log_run.match(file):
                os.system('mv ' + file + ' ' + logs_dir + '/' + timestamp + '_rundata.txt')

    finally:
        outf.close()

    return runs_data

# Testing parser for hpcg_gpu benchmark
def hpcg_gpu_parser(runs_data, out_file, timestamp, logs_dir):
    try:
        outf = open(out_file, mode='r')
        data = outf.read()
        z = re.search(r'final =\s+\d+\.\d+ GF', str(data))
        perf = re.search(r'(\d+\.\d+)', z.group()).group()
        runs_data.loc[timestamp,'PERFORMANCE'] = perf
        
        # Rename and move additional log files
        cwd = os.getcwd()
        log_res = re.compile(r'hpcg_log.*\.txt')
        log_run = re.compile(r'HPCG-Benchmark.*\.yaml')
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if log_res.match(file):
                    os.system('mv ' + file + ' ' + logs_dir + '/' + timestamp + '_residual.txt')
                if log_run.match(file):
                    os.system('mv ' + file + ' ' + logs_dir + '/' + timestamp + '_rundata.yaml')

    finally:
        outf.close()

    return runs_data


# Try matching the benchmark to a performance metric parser
def update_performance_metric(timestamp, benchmark, out_dir):
    csv_path = out_dir + '/runs.csv'
    out_file = out_dir + '/' + timestamp + '_out.txt'
    logs_dir = out_dir 

    runs_data = pd.read_csv(csv_path, index_col='TIMESTAMP')

    if benchmark == 'hello':
        updated_data = hello_parser(runs_data, out_file, timestamp)
    elif benchmark == 'hpcg_cpu':
        updated_data = hpcg_cpu_parser(runs_data, out_file, timestamp, logs_dir)
    elif benchmark == 'hpcg_gpu':
        updated_data = hpcg_gpu_parser(runs_data, out_file, timestamp, logs_dir)
    else:
        print('*** No parser found for ' + benchmark + ', skipping performance recording  ***')

    runs_data.to_csv(csv_path)
