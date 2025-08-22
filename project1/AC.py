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
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import AC_epy_block_1 as epy_block_1  # embedded python block
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
        self.sig_pwr = sig_pwr = 1
        self.samp_rate = samp_rate = 48000
        self.fc = fc = 1500
        self.deviation = deviation = 250
        self.EbN0_dB = EbN0_dB = 1000

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'input', False, True, '', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_edit_box_msg_0_win)
        self.epy_block_1 = epy_block_1.mc_sync_block()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, (int(samp_rate/symbol_rate)))
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-1))
        self.audio_sink_0 = audio.sink(samp_rate, "Speakers (2- Realtek(R) Audio)", True)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fc, 1, 0, 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2*math.pi*deviation/samp_rate))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'clear_input'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.epy_block_1, 'msg_in'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_char_to_float_0, 0))


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
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))

    def get_sig_pwr(self):
        return self.sig_pwr

    def set_sig_pwr(self, sig_pwr):
        self.sig_pwr = sig_pwr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*math.pi*self.deviation/self.samp_rate))
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate/self.symbol_rate)))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.analog_sig_source_x_1.set_frequency(self.fc)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.analog_frequency_modulator_fc_0.set_sensitivity((2*math.pi*self.deviation/self.samp_rate))

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
