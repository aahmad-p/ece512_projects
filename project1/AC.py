#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Acoustic Communication
# Author: AA, AV, OW
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import AC_epy_block_0 as epy_block_0  # embedded python block
import math
import sip



class AC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Acoustic Communication", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Acoustic Communication")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "AC")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 50
        self.sql_level2 = sql_level2 = -40
        self.sql_level = sql_level = -40
        self.sig_pwr = sig_pwr = 1
        self.samp_rate = samp_rate = 48000
        self.fc = fc = 1500
        self.deviation = deviation = 250
        self.EbN0_dB = EbN0_dB = 1000

        ##################################################
        # Blocks
        ##################################################

        self._sql_level2_range = qtgui.Range(-100, 100, 5, -40, 200)
        self._sql_level2_win = qtgui.RangeWidget(self._sql_level2_range, self.set_sql_level2, "'sql_level2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sql_level2_win)
        self._sql_level_range = qtgui.Range(-100, 100, 5, -40, 200)
        self._sql_level_win = qtgui.RangeWidget(self._sql_level_range, self.set_sql_level, "'sql_level'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sql_level_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            20000, #size
            samp_rate, #samp_rate
            'Sync Out', #name
            4, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-0.5, 0.5)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.05, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(True)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Binary Compare", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.epy_block_0 = epy_block_0.blk(start_pattern=[0,1,0,1,0,1], payload_length=80)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_ZERO_CROSSING,
            (int(samp_rate/symbol_rate)),
            0.05,
            1.0,
            1.0,
            100.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.channels_channel_model_2 = channels.channel_model(
            noise_voltage=3,
            frequency_offset=0.0,
            epsilon=1.001,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b([0,1], True, 1, [])
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_1_2 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_repeat_1_1 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_repeat_1_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_repeat_1 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_cc((int(samp_rate/symbol_rate)), symbol_rate/samp_rate, 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_cc((int(samp_rate/symbol_rate)), symbol_rate/samp_rate, 4000, 1)
        self.blocks_float_to_complex_0_2 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_2 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_float_0_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-1))
        self.analog_simple_squelch_cc_1_0 = analog.simple_squelch_cc(sql_level2, 1)
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc(sql_level, 1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fc, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (fc+deviation), 2, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (fc-deviation), 2, 0, 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2*math.pi*deviation/samp_rate))
        self.analog_agc_xx_0 = analog.agc_cc((1e-1), 1.0, 1, 20)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_1_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.blocks_repeat_1_0, 0))
        self.connect((self.blocks_char_to_float_0_0_0_0, 0), (self.blocks_repeat_1_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_time_sink_x_2, 2))
        self.connect((self.blocks_complex_to_real_2, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.analog_simple_squelch_cc_1, 0))
        self.connect((self.blocks_float_to_complex_0_1, 0), (self.analog_simple_squelch_cc_1_0, 0))
        self.connect((self.blocks_float_to_complex_0_2, 0), (self.channels_channel_model_2, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.blocks_repeat_1, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_repeat_1_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_repeat_1_1, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_repeat_1_2, 0), (self.qtgui_time_sink_x_2, 3))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_float_to_complex_0_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_float_to_complex_0_2, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0_0_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.channels_channel_model_2, 0), (self.blocks_complex_to_real_2, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.epy_block_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_repeat_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 1), (self.blocks_repeat_1_2, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_null_sink_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AC")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.blocks_moving_average_xx_0_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), self.symbol_rate/self.samp_rate)
        self.blocks_moving_average_xx_0_0_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), self.symbol_rate/self.samp_rate)
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_1.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_2.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.digital_symbol_sync_xx_0.set_sps((int(self.samp_rate/self.symbol_rate)))

    def get_sql_level2(self):
        return self.sql_level2

    def set_sql_level2(self, sql_level2):
        self.sql_level2 = sql_level2
        self.analog_simple_squelch_cc_1_0.set_threshold(self.sql_level2)

    def get_sql_level(self):
        return self.sql_level

    def set_sql_level(self, sql_level):
        self.sql_level = sql_level
        self.analog_simple_squelch_cc_1.set_threshold(self.sql_level)

    def get_sig_pwr(self):
        return self.sig_pwr

    def set_sig_pwr(self, sig_pwr):
        self.sig_pwr = sig_pwr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*math.pi*self.deviation/self.samp_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.blocks_moving_average_xx_0_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), self.symbol_rate/self.samp_rate)
        self.blocks_moving_average_xx_0_0_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), self.symbol_rate/self.samp_rate)
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_1.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_repeat_1_2.set_interpolation((int(self.samp_rate/self.symbol_rate)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.digital_symbol_sync_xx_0.set_sps((int(self.samp_rate/self.symbol_rate)))
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.analog_sig_source_x_0.set_frequency((self.fc-self.deviation))
        self.analog_sig_source_x_0_0.set_frequency((self.fc+self.deviation))
        self.analog_sig_source_x_1.set_frequency(self.fc)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*math.pi*self.deviation/self.samp_rate))
        self.analog_sig_source_x_0.set_frequency((self.fc-self.deviation))
        self.analog_sig_source_x_0_0.set_frequency((self.fc+self.deviation))

    def get_EbN0_dB(self):
        return self.EbN0_dB

    def set_EbN0_dB(self, EbN0_dB):
        self.EbN0_dB = EbN0_dB




def main(top_block_cls=AC, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
