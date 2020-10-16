# SeqScan-D

SeqScan-D is a novel algorithm for the summarization of sequences of temporally annotated symbolic locations, i.e. symbolic trajectories. A major example of symbolic trajectories are the sequences of Call Detail Records (CDR). SeqScan-D splits a trajectory in segments and replaces every segment with the symbolic location that is most representative in the period, based on density and temporal criteria. Unlike compression methods for symbolic sequences, for example based on RLE, SeqScan-D aims to preserve the significance of locations in time.  SeqScan-D is conceptually built on the SeqScan framework for the summarization of spatial trajectories.

# Citation
This algorithm is presented in the article:

Maria Luisa Damiani, Fatima Hachem, Christian Quadri, Matteo Rossini, and Sabrina Gaito (2020). On Location Relevance and Diversity in Human Mobility Data. ACM Transactions on Spatial Algorithms and Systems 7, 2, Article 7 (October 25, 2020), 38 pages. https://doi.org/10.1145/3423404"


# Code 

How to use the software:

It is sufficient to call the "seqscanD-scanner.py" from a command prompt. you will be asked to enter:
- The path for the input file, it has to be a csv file. This file requires at least two fields: "timestamp" and "location_name". Its detailed desctiption will be explained below.
- The path for the output file, it has to be a csv file too.
- The "N" parameter: the threshold for the algorithm's density criteria. It is an integer value.
- The "delta" parameter: the threshold for the algorithm's temporal criteria. It is a decimal value, in DAYS.

Structure of the input file:

The input file has to be in a CSV format. It refers to a single trajectory. It should include at least the two columns: "timestamp" and "location_name". The file shall have columns names as headers.
- The "timestamp" column: contains the timestamp of the corresponding point, by default the format is: "%Y-%m-%d %H:%M:%S". You may change the column name and the date format from the configuration file in: config/config.json
- The "location_name" column: contains the names or labels of the locations. You may change the required column name from the configuration file as well.

An example of the input file exists in: Data_examples/input.csv

Structure of the output file:

It is a CSV file composed of 6 fields:
- location_name
- start_time: the start time of the cluster (corresponding attractive location).
- end_time: the end time of the cluster.
- presence: The effective time spent inside the cluster (excluding the absences), in DAYS
- duration: The total time spent inside the cluster, in DAYS
- q_index: The stationarity index, is a clustering internal quality indicator, it takes a value between 0 and 1. For more information about this metric, please refer to [2] 

The fields names and the date format of the start_time and end_time values can be modified from the configuration file.

An example of the output file exists in: Data_examples/output.csv
The parameters used to obtain this output from the above input are: N= 4 points, delta= 0.0111 days (~15 mins)



