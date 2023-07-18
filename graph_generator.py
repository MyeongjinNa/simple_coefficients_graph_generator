
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from signal_name_handler import *

import numpy as np


class Visualize:
    def __init__(self, file_name, label_list):
        self.recording_name = file_name
        self.label_list = label_list
        self.scenario = 'highway'

    def plots_coefficient_graph_next_line(self, me_data, *Datas):
        confi_val_high_quality = 0.77

        me_color = 'tomato'
        sv_color = ['blue', 'green', 'fuchsia', 'pink']

        guiding_color = 'gray'
        cpp_color = 'fuchsia'

        fig = make_subplots(rows=6, cols=2,
                            shared_xaxes=True,
                            vertical_spacing=0.03,
                            horizontal_spacing=0.03,
                            specs=[[{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}]],
                            subplot_titles=('Neighbor Left', 'Neighbor Right')
                            )

        valid_log_dataset_num = 0

        for i in range(len(Datas)):
            for side in LaneSide:
                for signal in SignalName:
                    if 'SV.Next.{}.{}'.format(side.name, signal.name) in Datas[i].columns:
                        valid_log_dataset_num = valid_log_dataset_num + 1
                        fig.add_trace(trace=go.Scatter(x=Datas[i].index, y=Datas[i]['SV.Next.{}.{}'.format(side.name, signal.name)],
                                                       line=dict(color=sv_color[i]), name=self.label_list[i]+'_'+side.name+signal.name), row=int(signal.value), col=side.value)
        for side in LaneSide:
            for signal in SignalName:
                if 'ME.Next.{}.{}'.format(side.name, signal.name) in me_data.columns:
                    fig.add_trace(trace=go.Scatter(x=me_data.index,
                                                   y=me_data['ME.Next.{}.{}'.format(side.name, signal.name)],
                                                   line=dict(color=me_color),
                                                   name='me'+'_' + side.name + signal.name),
                                  row=int(signal.value), col=side.value)

        length = len(Datas[0].index)

        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.01), line=dict(color=guiding_color), showlegend=False),
                      row=2, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.0002), line=dict(color=guiding_color), showlegend=False),row=3, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.0002), line=dict(color=guiding_color), showlegend=False),
                      row=3, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,confi_val_high_quality), line=dict(color=guiding_color), showlegend=False),
                      row=6, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=2)

        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.0002), line=dict(color=guiding_color), showlegend=False),row=3, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.0002), line=dict(color=guiding_color), showlegend=False),
                      row=3, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,confi_val_high_quality), line=dict(color=guiding_color), showlegend=False),
                      row=6, col=2)

        fig['layout']['xaxis7']['title'] = 'Frame'
        fig['layout']['xaxis8']['title'] = 'Frame'
        fig['layout']['xaxis11']['title'] = 'Frame'
        fig['layout']['xaxis12']['title'] = 'Frame'
        fig['layout']['yaxis']['title'] = 'C0[m]'
        fig['layout']['yaxis3']['title'] = 'C1[rad]'
        fig['layout']['yaxis5']['title'] = 'C2[1/m]'
        fig['layout']['yaxis7']['title'] = 'C3[1/m^2]'
        fig['layout']['yaxis9']['title'] = 'View range(Start/End)[m]'
        fig['layout']['yaxis2']['title'] = 'C0[m]'
        fig['layout']['yaxis4']['title'] = 'C1[rad]'
        fig['layout']['yaxis6']['title'] = 'C2[1/m]'
        fig['layout']['yaxis8']['title'] = 'C3[1/m^2]'
        fig['layout']['yaxis10']['title'] = 'View range(Start/End)[m]'
        # fig['layout']['yaxis11']['title'] = 'Ego speed[kph]'
        fig['layout']['yaxis11']['title'] = 'Confidence(Quality)'
        fig['layout']['yaxis12']['title'] = 'Confidence(Quality)'
        fig['layout']['title'] = self.recording_name + ' ' + str(self.scenario)

        return fig

    def plots_coefficient_graph(self, me_data, cpp_data, *Datas):

        confi_val_high_quality = 0.77

        me_color = 'tomato'
        sv_color = ['blue', 'green', 'fuchsia', 'purple']

        guiding_color = 'gray'
        cpp_color = 'fuchsia'

        fig = make_subplots(rows=6, cols=2,
                            shared_xaxes=True,
                            vertical_spacing=0.03,
                            horizontal_spacing=0.03,
                            specs=[[{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}],
                                   [{}, {}]],
                            subplot_titles=('Ego Left', 'Ego Right')
                            )

        valid_log_dataset_num = 0

        for i in range(len(Datas)):
            for side in LaneSide:
                for signal in SignalName:
                    if 'SV.Host.{}.{}'.format(side.name, signal.name) in Datas[i].columns:
                        valid_log_dataset_num = valid_log_dataset_num + 1
                        fig.add_trace(trace=go.Scatter(x=Datas[i].index, y=Datas[i]['SV.Host.{}.{}'.format(side.name, signal.name)],
                                                       line=dict(color=sv_color[i]), name=self.label_list[i]+'_'+side.name+'_' +signal.name), row=int(signal.value), col=side.value)

        for side in LaneSide:
            for signal in SignalName:
                if 'ME.Host.{}.{}'.format(side.name, signal.name) in me_data.columns:
                    fig.add_trace(trace=go.Scatter(x=me_data.index,
                                                   y=me_data['ME.Host.{}.{}'.format(side.name, signal.name)],
                                                   line=dict(color=me_color),
                                                   name='ME'+'_' + side.name + '_' +signal.name),
                                  row=int(signal.value), col=side.value)

        for side in LaneSide:
            for signal in SignalName:
                if 'CPP.Host.{}'.format(signal.name) in cpp_data.columns:
                    fig.add_trace(trace=go.Scatter(x=cpp_data.index,
                                                   y=cpp_data['CPP.Host.{}'.format(signal.name)],
                                                   line=dict(color=cpp_color),
                                                   name='cpp' + '_' + signal.name),
                                  row=int(signal.value), col=side.value)

        length = len(Datas[0].index)

        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.01), line=dict(color=guiding_color), showlegend=False),
                      row=2, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.0002), line=dict(color=guiding_color), showlegend=False),row=3, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.0002), line=dict(color=guiding_color), showlegend=False),
                      row=3, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,confi_val_high_quality), line=dict(color=guiding_color), showlegend=False),
                      row=6, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.01), line=dict(color=guiding_color), showlegend=False),row=2, col=2)

        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.0002), line=dict(color=guiding_color), showlegend=False),row=3, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.0002), line=dict(color=guiding_color), showlegend=False),
                      row=3, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=1)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,-0.000002), line=dict(color=guiding_color), showlegend=False),
                      row=4, col=2)
        fig.add_trace(trace=go.Scatter(x=Datas[0].index, y=np.full(length,confi_val_high_quality), line=dict(color=guiding_color), showlegend=False),
                      row=6, col=2)

        fig['layout']['xaxis7']['title'] = 'Frame'
        fig['layout']['xaxis8']['title'] = 'Frame'
        fig['layout']['xaxis11']['title'] = 'Frame'
        fig['layout']['xaxis12']['title'] = 'Frame'
        fig['layout']['yaxis']['title'] = 'C0[m]'
        fig['layout']['yaxis3']['title'] = 'C1[rad]'
        fig['layout']['yaxis5']['title'] = 'C2[1/m]'
        fig['layout']['yaxis7']['title'] = 'C3[1/m^2]'
        fig['layout']['yaxis9']['title'] = 'View range(Start/End)[m]'
        fig['layout']['yaxis2']['title'] = 'C0[m]'
        fig['layout']['yaxis4']['title'] = 'C1[rad]'
        fig['layout']['yaxis6']['title'] = 'C2[1/m]'
        fig['layout']['yaxis8']['title'] = 'C3[1/m^2]'
        fig['layout']['yaxis10']['title'] = 'View range(Start/End)[m]'
        # fig['layout']['yaxis11']['title'] = 'Ego speed[kph]'
        fig['layout']['yaxis11']['title'] = 'Confidence(Quality)'
        fig['layout']['yaxis12']['title'] = 'Confidence(Quality)'
        fig['layout']['title'] = self.recording_name + ' ' + str(self.scenario)

        return fig

