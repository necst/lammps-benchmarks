# Spatial Arch Benchmarks

In this repo we collect results of different benchmarks and software on a range of architectures. `run_wrapper.py` is used to run a benchmark:

```
usage: run_wrapper.py [-h] --cmd CMD_STRING --bench BENCH_NAME --tag RUN_TAG
                      [--arch ARCH_INFO] [--dir DIR] [--gpu-power GPU_POWER]
                      [--cpu-power CPU_POWER] [--gpu-threshold GPU_THRESHOLD]
                      [--cpu-threshold CPU_THRESHOLD]

Run a benchmark program and record standard output and additional information

optional arguments:
  -h, --help            show this help message and exit
  --cmd CMD_STRING      [REQUIRED] Command used to run the benchmark, will be
                        recorded for reference
  --bench BENCH_NAME    [REQUIRED] Benchmark name. Is used to create a
                        subdirectory of the same name to store results
  --tag RUN_TAG         [REQUIRED] Shorthand for the name of the run. Is used
                        to plot graphs, so keep it short but meaningful
  --arch ARCH_INFO      [OPTIONAL] Allows to specify details on the
                        architecture. By default is the output of lscpu
  --dir DIR             [OPTIONAL] Allows to specify the directory where the
                        benchmark should be run, this script's directory by
                        default
  --gpu-power GPU_POWER
                        [OPTIONAL] Allows to monitor gpu power draw (requires
                        nvidia-smi)
  --cpu-power CPU_POWER
                        [OPTIONAL] Allows to monitor gpu power draw (requires
                        powerstat)
  --gpu-threshold GPU_THRESHOLD
                        [OPTIONAL] Allows to set a minimum threshold (Watt)
                        for GPU power average
  --cpu-threshold CPU_THRESHOLD
                        [OPTIONAL] Allows to set a minimum threshold (Watt)
                        for CPU power average
```

`erase_run.py` is used to erase data from a run while maintaining a consistent repo state:

```
usage: erase_run.py [-h] --timestamp TIMESTAMP --bench BENCH_NAME

Erase a benchmark run and keep the repo state clean and consistent

optional arguments:
  -h, --help            show this help message and exit
  --timestamp TIMESTAMP
                        [REQUIRED] Indexes the run to erase
  --bench BENCH_NAME    [REQUIRED] Speifies the benchmark for the run to erase
```

`generate_plots.py` is used to generate the graphs in /plots:

```
usage: generate_plots.py [-h] --x X_LIST --y Y_METRIC --y-name Y_NAME --x-name
                         X_NAME --x-label-pos X_LABEL_POS --name GRAPH_NAME
                         [--format FORMAT] [--bench-names BENCH_NAMES]
                         [--x-argsort X_SORT] [--y-mean Y_MEAN]

Plot different recorded metrics for a set of benchmark runs

optional arguments:
  -h, --help            show this help message and exit
  --x X_LIST            [REQUIRED] Command used to speciy x-axes as
                        BENCH_NAME:"TAG_REGEX"
  --y Y_METRIC          [REQUIRED] Command used to speciy which metric to plot
                        on the y axis
  --y-name Y_NAME       [REQUIRED] Command used to speciy which name to give
                        to the y axis
  --x-name X_NAME       [REQUIRED] Command used to speciy which name to give
                        to the x axis
  --x-label-pos X_LABEL_POS
                        [REQUIRED] Command used to speciy the position in the
                        regex, separated by '_', where the x axis label values
                        should be taken from, e.g. 1:2
  --name GRAPH_NAME     [REQUIRED] Command used to speciy the final graph name
  --format FORMAT       [OPTIONAL] Allows to specify the plot format (e.g.
                        svg,pdf)
  --bench-names BENCH_NAMES
                        [OPTIONAL] Allows to specify alternative names for the
                        benchmarks, e.g. NAME1:NAME2
  --x-argsort X_SORT    [OPTIONAL] If set to 1, sorts data accorfing to the
                        sorting of the x axis variable
  --y-mean Y_MEAN       [OPTIONAL] If set to 1, averages y values for data
                        with the same tag
```
