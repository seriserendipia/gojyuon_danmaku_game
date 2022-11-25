import time
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from gojyuon_danmaku_game import game_listening


class TestMainWindow(TestCase,QThread):
    testSignal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(TestMainWindow, self).__init__()
        self.ex_data = {
            "猫猫":"a"

        }

    def run(self):
        for i in self.ex_data.items():
            print(i)
            time.sleep(300)
            self.test_emit_message(i,i.key)


    def test_emit_message(self,message,uname):
        self.testSignal.emit(message, uname)

    def test_init_ui(self):
        self.fail()

    def test_init_qa_judger(self):
        self.fail()

    def test_on_shuffle_click(self):
        self.fail()

    def test_change_audio(self):
        self.fail()

    def test_get_audio_dir(self):
        self.fail()

    def test_update_chat(self):
        self.fail()

    def test_update_scoring(self):
        self.fail()

    def test_on_play_control_click(self):
        self.fail()

    def test_scoring_control(self):
        self.fail()

    def test_music_play_control(self):
        self.fail()

    def test_init_play_content(self):
        self.fail()

    def test_play_music(self):
        main_game.ListeningGame().play_music()

    def test_pause_music(self):
        self.fail()

    def test_timer_control(self):
        self.fail()

    def test_update_scoreing_label(self):
        self.fail()
