# SeqScan-D

SeqScan-D is a novel algorithm for the summarization of sequences of temporally annotated symbolic locations, i.e. symbolic trajectories. A major example of symbolic trajectories are the sequences of Call Detail Records (CDR). SeqScan-D splits a trajectory in segments and replaces every segment with the symbolic location that is the most representative in the period, based on density and temporal criteria. Unlike compression methods for symbolic sequences, for example based on RLE, SeqScan-D aims to preserve the significance of locations in time.  SeqScan-D is conceptually built on the SeqScan framework for the summarization of spatial trajectories.

# Citation
This algorithm is presented in the article:

Maria Luisa Damiani, Fatima Hachem, Christian Quadri, Matteo Rossini, and Sabrina Gaito (2020). On Location Relevance and Diversity in Human Mobility Data. ACM Transactions on Spatial Algorithms and Systems 7, 2, Article 7 (October 25, 2020), 38 pages. https://doi.org/10.1145/3423404"


# Code 

How to use the software:

Run "seqscanD-scanner.py" from a command prompt. you will be asked to enter:
- The path for the input file, as a csv file.
- The path for the output file, as a csv file.
- The "N" parameter: the threshold for the algorithm's density criteria. It is an integer value.
- The "delta" parameter: the threshold for the algorithm's temporal criteria. It is a decimal value, in DAYS.

INPUT FILE:

The input file specifies a single trajectory. A trajectory is a sequence of "timestamp" and "location_name" pairs. The file shall have these names as headers.
- "timestamp" : by default the format is "%Y-%m-%d %H:%M:%S". You may change the column name and the date format from the configuration file in: config/config.json
- "location_name": a string. You may change the required column name from the configuration file as well.

An example of input file  can be found in: Data_examples/input.csv

OUTPUT FILE:

The output file contains a sequence of records, one for each segment. A segment is described by the following fields:
- location_name: the most representative location in the segment.
- start_time/end_time: the start time and end time of the segment.
- weight of the segment expressed in DAYS.
- duration of the segment, in DAYS.
- q_index: the stationarity index (weight/duration). 

The fields names and the date format of the start_time and end_time values can be modified from the configuration file.

An example of output file can be found in: Data_examples/output.csv
The input parameters are: N= 4, delta= 0.0111 (~15 mins)



