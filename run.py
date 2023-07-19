import os
import pandas as pd
from logger import logger
from preprocessor import Preprocessor
from graph_generator import Visualize


class Run():
    def __init__(self, file_name, mobileye_path, log_csv_list, label_list, output_path,
                 EGO_GRAPH_GENERATION, CPP_GRAPH_GENERATION, NEIGHBOR_GRAPH_GENERATION, cpp_csv_path):
        self.file_name = os.path.basename(file_name)
        self.mobileye_path = mobileye_path
        self.log_csv_list = log_csv_list
        self.label_list = label_list
        self.output_path = output_path
        self.ego_graph_generation = EGO_GRAPH_GENERATION
        self.cpp_graph_generation = CPP_GRAPH_GENERATION
        self.neighbor_graph_generation = NEIGHBOR_GRAPH_GENERATION
        self.cpp_csv_path = cpp_csv_path
        self.vis = Visualize(self.file_name, self.label_list)

    def load_raw_data(self, file_path, label):
        """
        Rearrange the values by frameID from raw csv file
        :return: the data frame of log/can
        """
        if os.path.exists(file_path):
            arrg = Preprocessor()
            df = arrg.rearrangement(file_path)
            logger.debug('Preprocessing.. {}'.format(file_path))

        else:
            df = pd.DataFrame()
            logger.debug('Cannot find..{}'.format(label))

        return df

    def generate_coefficient_graph(self):
        # 1. Load log data
        sv_log_data_1 = self.load_raw_data(self.log_csv_list[0], self.label_list[0])
        sv_log_data_2 = self.load_raw_data(self.log_csv_list[1], self.label_list[1])
        sv_log_data_3 = self.load_raw_data(self.log_csv_list[2], self.label_list[2])
        sv_log_data_4 = self.load_raw_data(self.log_csv_list[3], self.label_list[3])

        # 2. Load mobileye data
        mobileye_data = self.load_raw_data(self.mobileye_path, 'mobileye')

        # 3. load cpp data
        if (self.cpp_graph_generation):
            cpp_data = self.load_raw_data(self.cpp_csv_path, 'cpp')
        else:
            cpp_data = pd.DataFrame()

        # 4. Generate the graph as html
        if (self.ego_graph_generation):
            fig = self.vis.plots_coefficient_graph(mobileye_data, cpp_data,
                                                   sv_log_data_1, sv_log_data_2, sv_log_data_3, sv_log_data_4)
            fig.show()
            fig.write_html(os.path.join(self.output_path,
                                        self.file_name + '_' + self.label_list[0] + '_' + self.label_list[1] + '_ego_graph.html'))

        if (self.neighbor_graph_generation):
            fig = self.vis.plots_coefficient_graph_next_line(mobileye_data,
                                                             sv_log_data_1, sv_log_data_2, sv_log_data_3, sv_log_data_4)
            fig.show()
            fig.write_html(os.path.join(self.output_path,
                                        self.file_name + '_' + self.label_list[0] + '_' + self.label_list[1] + '_neighbor_graph.html'))

