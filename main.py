from logger import logger
import getpass
from run import Run
import os

DEBUG_FILE_NAME = r"//10.10.21.126/adaf_data/001_DB/1_Vehicle_Road/2020_Mini_Endurance_Run_1050/adaf/Recorder_2020-11-02_15-46-41"
DEBUG_CAM_PARAM = r"//10.10.21.126/adaf_data/04_Endurance_Run/2020_Mini_Endurance_Run_1050/cam_param_DN8(1920x1080).txt"
DEBUG_FRAME_LIMIT = "0"
DEBUG_CAN_DATA_PATH = r"//10.10.21.126/adaf_data/001_DB/1_Vehicle_Road/2020_Mini_Endurance_Run_1050/adaf/Recorder_2020-11-02_15-46-41/Recorder_2020-11-02_15-46-41_can.csv"
DEBUG_MOBILEYE_PATH = r"//10.10.21.126/adaf_data/001_DB/1_Vehicle_Road/2020_Mini_Endurance_Run_1050/adaf/Recorder_2020-11-02_15-46-41/Recorder_2020-11-02_15-46-41_me.csv"

DEBUG_LOG_CSV_PATH_1 = r'//10.10.21.126/adaf_data\02_Log_Release\adaf_lde_log\ADAFDEV_230509_adaf_integration(017c162)_ADAF_R18.0_LD_R1.9.1_RE\log_sv\Recorder_2020-11-02_15-46-41_log\Recorder_2020-11-02_15-46-41_lda_tiny_log.csv'
LABEL_1 = 'log_1'

DEBUG_LOG_CSV_PATH_2 = r''
LABEL_2 = 'log_2'

DEBUG_LOG_CSV_PATH_3 = r''
LABEL_3 = 'log_3'

DEBUG_LOG_CSV_PATH_4 = r''
LABEL_4 = 'log_4'

OUTPUT_PATH = os.getcwd()

EGO_GRAPH_GENERATION = True
NEIGHBOR_GRAPH_GENERATION = True

CPP_GRAPH_GENERATION = False
CPP_CSV_PATH = r'//10.10.21.126/adaf_data\02_Log_Release\adaf_lde_log\ADAFDEV_230509_adaf_integration(017c162)_ADAF_R18.0_LD_R1.9.1_RE\log_sv\Recorder_2020-11-02_15-46-41_log\Recorder_2020-11-02_15-46-41_adaf_log.csv'

if __name__ == '__main__':

    logger.info(getpass.getuser())
    logger.info("Start")

    logger.info('Output Path :   %s' % OUTPUT_PATH)

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    log_csv_list = [DEBUG_LOG_CSV_PATH_1, DEBUG_LOG_CSV_PATH_2, DEBUG_LOG_CSV_PATH_3, DEBUG_LOG_CSV_PATH_4]
    label_list = [LABEL_1, LABEL_2, LABEL_3, LABEL_4]

    run = Run(DEBUG_FILE_NAME, DEBUG_FRAME_LIMIT, DEBUG_CAN_DATA_PATH, DEBUG_MOBILEYE_PATH, log_csv_list, label_list,
              OUTPUT_PATH, EGO_GRAPH_GENERATION, CPP_GRAPH_GENERATION, NEIGHBOR_GRAPH_GENERATION,
              CPP_CSV_PATH)

    run.generate_coefficient_graph()
    logger.info("End")

