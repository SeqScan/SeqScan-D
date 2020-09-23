# Discrete-SeqScan-clustering
SeqScan-D: cluster-based technique for the segmentation of symbolic trajectories. 

The goal is to extract from a symbolic trajectory a series of temporally annotated locations, qualified as attractive.
A location is attractive when the user spends inside of it at least some amount of time, with possibility of some occasional absences.
The algorithm requires 2 parameters:
- delta (minimum amount of time effiectively spent inside the location, i.e without the absences) and 
- N (minimum number of points occured inside the location)

SeqScan-D takes inspiration from SeqScan, but while the latter is tailored to spatial trajectories, SeqScan-D is to be applied on symbolic trajectories (like Call Details Records CDR).
For details please refer to: M. L. Damiani, F. Hachem, C. Quadri, M. Rossini, and S. Gaito.  On location relevance and diversity in human mobility data. ACM TSAS, In press.

How to use the software:
It is sufficient to call the "seqscanD-scanner.py" from a command prompt. you will be asked to enter:
- The path for the input file, it has to be a csv file. This file requires at least two fields: "timestamp" and "site_name". The detailed desctiption will be explained below.
- The path for the output file, it has to be a csv file too.
- The "N" parameter: it is an integer value.
- The "delta" parameter: it is a decimal value, in DAYS.

Structure of the input file:
The input file has to be in a CSV format. It refers to a single trajectory. It should include at least the two columns: "timestamp" and "location_name". The file has to have columns names as headers.
- The "timesptamp"column: contains the date and time of the corresponding point, by default it has to be in the format of: "%Y-%m-%d %H:%M:%S". You may change the column name and the date format from the configuration file in: config/config.json
- The "location_name" column: contains the names or labels of the locations. You may change the required column name from the configuration file as well.

An example of the input file exists in: Data_examples/input.csv

Structure of the output file:
It is a CSV file composed of 6 fields:
- location_name
- start_time: the start time of the cluster (corresponding attractive location).
- end_time: the end time of the cluster.
- presence: The effective time spent inside the cluster (excluding the absences), in DAYS
- duration: The total time spent inside the cluster, in DAYS
- q_index: The stationnarity index, a decimal value between 0 and 1 that helps evaluating the quality of the clusters. For more information about this metric, please refer to: Damiani, M. L., Issa, H., Fotino, G., Heurich, M., & Cagnacci, F. (2016). Introducing ‘presence’and ‘stationarity index’to study partial migration patterns: an application of a spatio-temporal clustering technique. International Journal of Geographical Information Science, 30(5), 907-928.

The fields names and the date format of the start_time and end_time values can be modified from the configuration file.

An example of the output file exists in: Data_examples/output.csv
The parameters used to obtain this output from the above input are: N= 4 points, delta= 0.0111 days (~15 mins)



