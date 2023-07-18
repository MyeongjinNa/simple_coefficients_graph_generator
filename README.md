# simple_coefficients_graph_generator

This tool is for generating the coefficients graph of the polynomials compared with Mobileye.

## Getting Started

To run this tool, you'll need to have Python 3.x installed. You can install the required Python packages using pip and the requirements.txt file.

    pip install -r requirements.txt


### Arguments

|**Argument**|**Description**|**Type**|
| ------- | ------- | ------- |
| DEBUG_FILE_NAME |path to measurement directory | string | 
| DEBUG_MOBILEYE_PATH |path to Mobileye CSV file, you can leave blank|string|
| DEBUG_LOG_CSV_PATH_1 |path to Log CSV file(lda_tiny_log.csv)|string|
| DEBUG_LOG_CSV_PATH_2 |path to Log CSV file(lda_tiny_log.csv), you can leave blank|string|
| DEBUG_LOG_CSV_PATH_3 |path to Log CSV file(lda_tiny_log.csv), you can leave blank|string|
| DEBUG_LOG_CSV_PATH_4 |path to Log CSV file(lda_tiny_log.csv), you can leave blank|string|
| LABEL_1 |label of DEBUG_LOG_CSV_PATH_1 in graph|string|
| LABEL_2 |label of DEBUG_LOG_CSV_PATH_2 in graph, you can leave blank|string|
| LABEL_3 |label of DEBUG_LOG_CSV_PATH_3 in graph, you can leave blank|string|
| LABEL_4 |label of DEBUG_LOG_CSV_PATH_4 in graph, you can leave blank|string|
| OUTPUT_PATH |output path to write a graph|True|string|
| EGO_GRAPH_GENERATION |check if the coefficients graph of ego line |boolean|
| NEIGHBOR_GRAPH_GENERATION |check if the coefficients graph of neighbor line |boolean|
| CPP_GRAPH_GENERATION |check if the coefficients graph of cpp line |boolean|
| CPP_CSV_PATH |path to Log CSV file(adaf_log.csv), you can leave blank|boolean|
