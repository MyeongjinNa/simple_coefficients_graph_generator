import numpy as np
import pandas as pd
import os
from logger import logger
import glob
from pandas.core.common import SettingWithCopyWarning


import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

is_rb_output = False


# Define necessary protocol name
class ProtocolName:
    lda : str = 'drv_segment_C0'
    cpp : str = 'cpp_ego_lane_coefficient_0'
    mobileye : str = 'LaneMarkPosition_C0_Lh_ME'
    ccan : str = 'YAW_RATE'
    dgps : str = 'AngRateZ'


class Preprocessor:
    def __init__(self):
        self.necessary_signal_name = ProtocolName
        self.necessary_suffix = '_log.csv'


    def rearrangement(self, file_path):

        if self.necessary_suffix in file_path:
            df = pd.read_csv(file_path, index_col=False, low_memory=False, error_bad_lines=False)
        else: # pcan
            df = pd.read_csv(file_path, index_col=False, header=1, low_memory=False)

        if self.necessary_signal_name.lda in df.columns:
            data = self.rearrangement_log(file_path)

        elif self.necessary_signal_name.cpp in df.columns:
            data = self.rearrangement_cpp(file_path)

        elif self.necessary_signal_name.mobileye in df.columns:
            data = self.rearrangement_mobileye(file_path)

        elif self.necessary_signal_name.ccan in df.columns:
            data = self.rearrangement_can(file_path)

        elif self.necessary_signal_name.dgps in df.columns:
            data = self.rearrangement_dgps(file_path)

        del df

        return data

    def rearrangement_log(self, file_path):
        log_df = pd.DataFrame()
        origin_log_df = pd.read_csv(file_path, index_col=False, low_memory=False, error_bad_lines=False)
        drv_log_df = origin_log_df.drop(
            labels=['rb_color', 'rb_position', 'rb_type', 'rb_trackingID', 'rb_enable', 'rb_multiple',
                    'rb_roadBoundaryType', 'rb_vcs_start', 'rb_vcs_end', 'rb_vcs_predicted_start',
                    'rb_vcs_predicted_end', 'rb_lineWidthModel_C0', 'rb_lineWidthModel_C1', 'rb_segment_num',
                    'rb_segment_start', 'rb_segment_end', 'rb_segment_C0', 'rb_segment_C1',
                    'rb_segment_C2', 'rb_segment_C3', 'drv_lines_num', 'drv_segment_start',
                    'drv_segment_end','rb_lines_num', 'num_of_merged_point', 'merge_pos_lon', 'num_of_branch_point',
                    # 'branch_pos_lon'
                    ], axis=1) #'rb_lines_num', 'num_of_merged_point', 'merge_pos_lon', 'num_of_branch_point',


        # Get Host Left line with drv_position is 3.0 And drv_multiple is 1.0
        host_left_df = drv_log_df.loc[
            (drv_log_df.drv_position == 3.0) & (drv_log_df.drv_multiple == 1.0)]
        host_left_df = self.arrange(drv_log_df, host_left_df, 'Host.LH')

        # Get Host Right line with drv_position is 4.0 And drv_multiple is 1.0
        host_right_df = drv_log_df.loc[
            (drv_log_df.drv_position == 4.0) & (drv_log_df.drv_multiple == 1.0)]
        host_right_df = self.arrange(drv_log_df, host_right_df, 'Host.RH')

        # Get Next Left Line with drv_position is 5.0 And drv_multiple is 1.0
        next_left_df = drv_log_df.loc[
            (drv_log_df.drv_position == 2.0) & (drv_log_df.drv_multiple == 1.0)]
        next_left_df = self.arrange(drv_log_df, next_left_df, 'Next.LH')

        # Get Next Right Line with drv_position is 5.0 And drv_multiple is 1.0
        next_right_df = drv_log_df.loc[
            (drv_log_df.drv_position == 5.0) & (drv_log_df.drv_multiple == 1.0)]
        next_right_df = self.arrange(drv_log_df, next_right_df, 'Next.RH')

        if is_rb_output:
            rb_log_df = origin_log_df.drop(
                labels=['drv_color', 'drv_position', 'drv_type', 'drv_trackingId', 'drv_enable', 'drv_multiple',
                        'drv_roadBoundaryType', 'drv_vcs_start', 'drv_vcs_end', 'drv_vcs_predicted_start',
                        'drv_vcs_predicted_end', 'drv_lineWidthModel_C0', 'drv_lineWidthModel_C1', 'drv_segment_num',
                        'drv_segment_start', 'drv_segment_end', 'drv_segment_C0', 'drv_segment_C1',
                        'drv_segment_C2', 'drv_segment_C3', 'drv_lines_num', 'drv_segment_start',
                        'drv_segment_end', 'rb_lines_num', 'num_of_merged_point', 'merge_pos_lon', 'num_of_branch_point',
                        'rb_segment_start',
                                         'rb_segment_end',
                        # 'branch_pos_lon'
                        ], axis=1) #'rb_lines_num', 'num_of_merged_point', 'merge_pos_lon', 'num_of_branch_point',


            for i, val in enumerate(rb_log_df.rb_trackingID.unique()):
                rb_df = rb_log_df.loc[(rb_log_df.rb_trackingID == val) & (rb_log_df.rb_multiple == 0.0)]
                rb_df = self.arrange_roadboundary(rb_log_df, rb_df, f'Rb_{i}')
                log_df = pd.concat([log_df, rb_df], axis=1)

        # Concat all host and next line values
        log_df = pd.concat(
            [host_left_df, host_right_df, next_left_df, next_right_df, log_df],
            axis=1)

        return log_df

    def arrange(self, origin_df, df, str):

        # origin_df.reset_index(inplace=True, drop=False)
        df.reset_index(inplace=True, drop=True)
        empty = pd.DataFrame(index=range(0, 1), columns=df.columns)
        empty.fillna(-1, inplace=True)

        for i in range(int(origin_df['frame_id'].max()) + 1):
            if i < len(df):
                if i == int(df.at[i, 'frame_id']):
                    pass
                elif i != int(df.at[i, 'frame_id']):
                    temp1 = df.iloc[df.index < i, :]
                    temp2 = df.iloc[df.index >= i, :]
                    df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                    df.at[i, 'frame_id'] = i
                    df.at[i, 'ocPitch'] = origin_df.at[origin_df.at[i, 'frame_id'], 'ocPitch']
                    df.iloc[i, 3:] = -1
            else:
                temp1 = df.iloc[df.index < i, :]
                temp2 = df.iloc[df.index >= i, :]
                df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                df.at[i, 'frame_id'] = i
                df.at[i, 'ocPitch'] = origin_df.at[origin_df.at[i, 'frame_id'], 'ocPitch']
                df.iloc[i, 3:] = -1

        df.reset_index(inplace=True, drop=True)

        df.rename(columns={'drv_color': 'SV.{}.drv_color'.format(str), 'drv_position': 'SV.{}.drv_position'.format(str),
                           'drv_type': 'SV.{}.drv_type'.format(str),
                           'drv_trackingID': 'SV.{}.drv_trackingID'.format(str),
                           'drv_enable': 'SV.{}.drv_enable'.format(str),
                           'drv_multiple': 'SV.{}.drv_multiple'.format(str),
                           'drv_roadBoundaryType': 'SV.{}.drv_roadBoundaryType'.format(str),
                           'drv_lineWidthModel_C0': 'SV.{}.drv_lineWidthModel_C0'.format(str),
                           'drv_lineWidthModel_C1': 'SV.{}.drv_lineWidthModel_C1'.format(str),
                           'drv_segment_num': 'SV.{}.drv_segment_num'.format(str),

                           'drv_vcs_start': 'SV.{}.Start'.format(str),
                           'drv_vcs_end': 'SV.{}.End'.format(str),
                           'drv_vcs_predicted_start': 'SV.{}.ViewRangeStart'.format(str),
                           'drv_vcs_predicted_end': 'SV.{}.ViewRangeEnd'.format(str),

                           'ocPitch': 'oc.Pitch',

                           'drv_segment_C0': 'SV.{}.C0'.format(str),
                           'drv_segment_C1': 'SV.{}.C1'.format(str),
                           'drv_segment_C2': 'SV.{}.C2'.format(str),
                           'drv_segment_C3': 'SV.{}.C3'.format(str),
                           'confidence': 'SV.{}.Confidence'.format(str),
                           'confidence ': 'SV.{}.Confidence'.format(str),
                           'confidenceLevel' : 'SV.{}.Quality'.format(str),
                           }, inplace=True)

        return df

    def arrange_roadboundary(self, origin_df, df, str):

        # origin_df.reset_index(inplace=True, drop=False)
        df.reset_index(inplace=True, drop=True)
        empty = pd.DataFrame(index=range(0, 1), columns=df.columns)
        empty.fillna(-1, inplace=True)

        for i in range(int(origin_df['frame_id'].max()) + 1):
            if i < len(df):
                if i == int(df.at[i, 'frame_id']):
                    pass
                elif i != int(df.at[i, 'frame_id']):
                    temp1 = df.iloc[df.index < i, :]
                    temp2 = df.iloc[df.index >= i, :]
                    df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                    df.at[i, 'frame_id'] = i
                    df.at[i, 'ocPitch'] = origin_df.at[origin_df.at[i, 'frame_id'], 'ocPitch']
                    df.iloc[i, 3:] = -1
            else:
                temp1 = df.iloc[df.index < i, :]
                temp2 = df.iloc[df.index >= i, :]
                df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                df.at[i, 'frame_id'] = i
                df.at[i, 'ocPitch'] = origin_df.at[origin_df.at[i, 'frame_id'], 'ocPitch']
                df.iloc[i, 3:] = -1

        df.reset_index(inplace=True, drop=True)

        df.rename(columns={'rb_color': 'SV.{}.rb_color'.format(str),
                           'rb_position': 'SV.{}.rb_position'.format(str),
                           'rb_type': 'SV.{}.rb_type'.format(str),
                           'rb_trackingID': 'SV.{}.rb_trackingID'.format(str),
                           'rb_enable': 'SV.{}.rb_enable'.format(str),
                           'rb_multiple': 'SV.{}.rb_multiple'.format(str),
                           'rb_roadBoundaryType': 'SV.{}.rb_roadBoundaryType'.format(str),
                           'rb_lineWidthModel_C0': 'SV.{}.rb_lineWidthModel_C0'.format(str),
                           'rb_lineWidthModel_C1': 'SV.{}.rb_lineWidthModel_C1'.format(str),
                           'rb_segment_num': 'SV.{}.rb_segment_num'.format(str),

                           'rb_vcs_start': 'SV.{}.Start'.format(str),
                           'rb_vcs_end': 'SV.{}.End'.format(str),
                           'rb_vcs_predicted_start': 'SV.{}.ViewRangeStart'.format(str),
                           'rb_vcs_predicted_end': 'SV.{}.ViewRangeEnd'.format(str),

                           'ocPitch': 'oc.Pitch',

                           'rb_segment_C0': 'SV.{}.C0'.format(str),
                           'rb_segment_C1': 'SV.{}.C1'.format(str),
                           'rb_segment_C2': 'SV.{}.C2'.format(str),
                           'rb_segment_C3': 'SV.{}.C3'.format(str),
                           'confidence': 'SV.{}.Confidence'.format(str),
                           'confidence ': 'SV.{}.Confidence'.format(str),
                           'confidenceLevel' : 'SV.{}.Quality'.format(str),
                           }, inplace=True)

        return df

    def rearrangement_cpp(self, log_file_path):

        logger.debug(log_file_path)
        origin_log_df = pd.read_csv(log_file_path, index_col=False, low_memory=False, error_bad_lines=False)
        origin_log_df.drop(
            labels=['obj_id', 'obj_type', 'obj_confidence', 'BB_x1', 'BB_y1', 'BB_x2', 'BB_y2', 'far_BB_x1',
                    'far_BB_x2',
                    'far_BB_x3', 'far_BB_x4', 'far_BB_y1', 'far_BB_y2', 'far_BB_y3', 'far_BB_y4', 'near_BB_x1',
                    'near_BB_x2',
                    'near_BB_x3', 'near_BB_x4', 'near_BB_y1', 'near_BB_y2', 'near_BB_y3', 'near_BB_y4', 'long_dist',
                    'lat_dist', 'dist_validity', 'rel_long_vel', 'rel_lat_vel', 'lane_assignment', 'lane_change',
                    'motion_status',
                    'motion_category', 'motion_orientation', 'cipv_id', 'cipv_tracked', 'cipv_lost', 'cinvl_id',
                    'cinvl_tracked',
                    'cinvr_id', 'cinvr_tracked', 'heading_angle', 'tracking_age', 'ttc', 'opi_headingAngle_status'],
            axis=1, inplace=True)
        cpp_df = origin_log_df.drop_duplicates(['frame_id'])
        cpp_df.reset_index(inplace=True, drop=False)

        empty = pd.DataFrame(index=range(0, 1), columns=origin_log_df.columns)
        empty.fillna(-1, inplace=True)
        for i in range(int(origin_log_df['frame_id'].max()) + 1):
            if i < len(cpp_df):
                if (i == int(cpp_df.at[i, 'frame_id'])):
                    pass
                elif (i != int(cpp_df.at[i, 'frame_id'])):
                    temp1 = cpp_df.iloc[cpp_df.index < i, :]
                    temp2 = cpp_df.iloc[cpp_df.index >= i, :]
                    cpp_df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                    cpp_df.at[i, 'frame_id'] = i

                    cpp_df.iloc[i, 3:] = -1
            else:
                temp1 = cpp_df.iloc[cpp_df.index < i, :]
                temp2 = cpp_df.iloc[cpp_df.index >= i, :]
                cpp_df = temp1.append(empty, ignore_index=True).append(temp2, ignore_index=True)
                cpp_df.at[i, 'frame_id'] = i

                cpp_df.iloc[i, 3:] = -1

        cpp_df.reset_index(inplace=True, drop=True)

        cpp_df.rename(columns={'cpp_ego_lane_confidence': 'CPP.Host.Confidence',
                               'cpp_ego_lane_view_range': 'CPP.Host.ViewRangeEnd',
                               'cpp_ego_lane_coefficient_0': 'CPP.Host.C0',
                               'cpp_ego_lane_coefficient_1': 'CPP.Host.C1',
                               'cpp_ego_lane_coefficient_2': 'CPP.Host.C2',
                               'cpp_ego_lane_coefficient_3': 'CPP.Host.C3'}, inplace=True)
        cpp_df.fillna(-1, inplace=True)

        return cpp_df

    def rearrangement_mobileye(self, file_path):

        df = pd.read_csv(file_path, index_col=False, header=1, low_memory=False)
        if 'CAM_FC' in df.columns:

            df = pd.concat([df.iloc[:, 0:8], df.iloc[:, 8:-1].fillna(method='ffill')], axis=1)

            df = df.dropna(subset=['CAM_FC'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_FC', 'CAM_SR', 'CAM_SL', 'CAM_SVM_F', 'CAM_SVM_R', 'CAM_SVM_L', 'CAM_SVM_B'],
                          axis=1, inplace=True)

        elif 'CAM_1' in df.columns:

            df = pd.concat([df.iloc[:, 0:21], df.iloc[:, 21:-1].fillna(method='ffill')], axis=1)

            df = df.dropna(subset=['CAM_1'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_{}'.format(i) for i in range(1, 21)], axis=1, inplace=True)

        df.rename(columns={'Time': 'ME.Timestamp', 'LaneMarkModelA_C2_Lh_ME': 'ME.Host.LH.C2',
                               'LaneMarkPosition_C0_Lh_ME': 'ME.Host.LH.C0',
                               'LaneMarkHeadingAngle_C1_Lh_ME': 'ME.Host.LH.C1',
                               'LaneMarkModelDerivA_C3_Lh_ME': 'ME.Host.LH.C3', 'LaneMarkModelA_C2_Rh_ME': 'ME.Host.RH.C2',
                               'LaneMarkPosition_C0_Rh_ME': 'ME.Host.RH.C0',
                               'LaneMarkHeadingAngle_C1_Rh_ME': 'ME.Host.RH.C1',
                               'LaneMarkModelDerivA_C3_Rh_ME': 'ME.Host.RH.C3',
                               'Lh_View_End_Longitudinal_Dist': 'ME.Host.LH.ViewRangeEnd',
                               'Rh_View_End_Longitudinal_Dist': 'ME.Host.RH.ViewRangeEnd',
                               'Lh_View_Start_Longitudinal_Dist': 'ME.Host.LH.ViewRangeStart',
                               'Rh_View_Start_Longitudinal_Dist': 'ME.Host.RH.ViewRangeStart',

                               'Lh_Neightbor_Avail': 'ME.Neighbor.LH.Available',

                               'Quality_Lh_ME': 'ME.Host.LH.Quality',
                               'Quality_Rh_ME': 'ME.Host.RH.Quality',

                           'LaneMark_Confidence_Lh_ME':'ME.Host.LH.Confidence',
                           'LaneMark_Confidence_Rh_ME': 'ME.Host.RH.Confidence',

                               'Lh_Neighbor_LaneMark_Model_A_C2': 'ME.Next.LH.C2',
                               'Lh_Neighbor_LaneMark_Model_B_C1': 'ME.Next.LH.C1',
                               'Lh_Neighbor_LaneMark_Model_dA_C3': 'ME.Next.LH.C3',
                               'Lh_Neighbor_LaneMark_Pos_C0': 'ME.Next.LH.C0',
                               'Rh_Neighbor_LaneMark_Model_A_C2': 'ME.Next.RH.C2',
                               'Rh_Neighbor_LaneMark_Model_B_C1': 'ME.Next.RH.C1',
                               'Rh_Neighbor_LaneMark_Model_dA_C3': 'ME.Next.RH.C3',
                               'Rh_Neighbor_LaneMark_Pos_C0': 'ME.Next.RH.C0',
                               'Lh_Neightbor_Type': 'ME.Next.LH.Type',

                                'Rh_Neightbor_Type': 'ME.Next.RH.Type',
                               'Classification_Lh_ME': 'ME.Host.LH.Classification',
                               'Classification_Rh_ME': 'ME.Host.RH.Classification',
                               'Marker_Width_Lh_ME': 'ME.Host.LH.MarkerWidth',
                               'Marker_Width_Rh_ME': 'ME.Host.RH.MarkerWidth'
                               }, inplace=True)

        df.fillna(-1, inplace=True)
        df['ME.Host.LH.C0'] = -df['ME.Host.LH.C0']
        df['ME.Host.LH.C1'] = -df['ME.Host.LH.C1']
        df['ME.Host.LH.C2'] = -df['ME.Host.LH.C2']
        df['ME.Host.LH.C3'] = -df['ME.Host.LH.C3']

        df['ME.Host.RH.C0'] = -df['ME.Host.RH.C0']
        df['ME.Host.RH.C1'] = -df['ME.Host.RH.C1']
        df['ME.Host.RH.C2'] = -df['ME.Host.RH.C2']
        df['ME.Host.RH.C3'] = -df['ME.Host.RH.C3']

        df['ME.Next.LH.C0'] = -df['ME.Next.LH.C0']
        df['ME.Next.LH.C1'] = -df['ME.Next.LH.C1']
        df['ME.Next.LH.C2'] = -df['ME.Next.LH.C2']
        df['ME.Next.LH.C3'] = -df['ME.Next.LH.C3']

        df['ME.Next.RH.C0'] = -df['ME.Next.RH.C0']
        df['ME.Next.RH.C1'] = -df['ME.Next.RH.C1']
        df['ME.Next.RH.C2'] = -df['ME.Next.RH.C2']
        df['ME.Next.RH.C3'] = -df['ME.Next.RH.C3']

        if 'ME.Host.LH.ViewRangeEnd' in df.columns:
            df['ME.Next.LH.ViewRangeEnd'] = df['ME.Host.LH.ViewRangeEnd']
        if 'ME.Host.LH.ViewRangeStart' in df.columns:
            df['ME.Next.LH.ViewRangeStart'] = df['ME.Host.LH.ViewRangeStart']

        if 'ME.Host.RH.ViewRangeEnd' in df.columns:
            df['ME.Next.RH.ViewRangeEnd'] = df['ME.Host.RH.ViewRangeEnd']
        if 'ME.Host.RH.ViewRangeStart' in df.columns:
            df['ME.Next.RH.ViewRangeStart'] = df['ME.Host.RH.ViewRangeStart']

        if 'ME.Host.LH.Confidence' in df.columns:
            df['ME.Next.LH.Confidence'] = df['ME.Host.LH.Confidence']
        if 'ME.Host.LH.Quality' in df.columns:
            df['ME.Next.LH.Quality'] = df['ME.Host.LH.Quality']
        if 'ME.Host.RH.Confidence' in df.columns:
            df['ME.Next.RH.Confidence'] = df['ME.Host.RH.Confidence']
        if 'ME.Host.RH.Quality' in df.columns:
            df['ME.Next.RH.Quality'] = df['ME.Host.RH.Quality']

        df.fillna(-1, inplace=True)

        return df

    def rearrangement_dgps(self, file_path):
        df = pd.read_csv(file_path, index_col=False, header=1, low_memory=False)

        if 'CAM_FC' in df.columns:
            df = pd.concat([df.iloc[:, 0:8], df.iloc[:, 8:-1].fillna(method='ffill')], axis=1)
            df = df.dropna(subset=['CAM_FC'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_FC', 'CAM_SR', 'CAM_SL', 'CAM_SVM_F', 'CAM_SVM_R', 'CAM_SVM_L', 'CAM_SVM_B'],
                          axis=1, inplace=True)

        elif 'CAM_1' in df.columns:
            df = pd.concat([df.iloc[:, 0:21], df.iloc[:, 21:-1].fillna(method='ffill')], axis=1)
            df = df.dropna(subset=['CAM_1'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_{}'.format(i) for i in range(1, 21)], axis=1, inplace=True)

        df.rename(columns={'Time': 'DGPS.Timestamp','Speed2D': 'VDY.EgoSpeed'}, inplace=True)
        df.fillna(-1, inplace=True)

        return df

    def rearrangement_can(self, file_path):
        df = pd.read_csv(file_path, index_col=False, header=1, low_memory=False)

        if 'CAM_FC' in df.columns:

            df = pd.concat([df.iloc[:, 0:8], df.iloc[:, 8:-1].fillna(method='ffill')], axis=1)
            df = df.dropna(subset=['CAM_FC'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_FC', 'CAM_SR', 'CAM_SL', 'CAM_SVM_F', 'CAM_SVM_R', 'CAM_SVM_L', 'CAM_SVM_B'],
                          axis=1, inplace=True)

        elif 'CAM_1' in df.columns:
            df = pd.concat([df.iloc[:, 0:21], df.iloc[:, 21:-1].fillna(method='ffill')], axis=1)

            df = df.dropna(subset=['CAM_1'])
            df.reset_index(drop=True, inplace=True)
            df.drop(['CAM_{}'.format(i) for i in range(1, 21)], axis=1, inplace=True)

        df.rename(columns={'Time': 'CAN.Timestamp','Speed2D': 'VDY.EgoSpeed',}, inplace=True)

        df.fillna(-1, inplace=True)

        return df
