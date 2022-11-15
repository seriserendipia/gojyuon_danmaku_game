import random
import string
import sys
import time

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from gojyuon_danmaku_game import initdata
from gojyuon_danmaku_game.main_game import MainWindow
from initdata import hiragana


class TestMainWindow(QThread):
    testSignal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(TestMainWindow, self).__init__()
        self.ex_data = [("猫猫","a")]

        name_list = ["狗子","鲸鱼","大兔子","垂耳兔","黑兔","朱迪","尼克","闪电","棉花糖","泡泡","水母",
                     "章鱼哥","派大星","夏奇拉","狼先生","狼太太","小灰灰","绵羊","山羊","羚羊","瞪羚",
                     "豹子","仓仓","鼠鼠","大白鼠","米老鼠","妙妙米奇","快乐星球","小兔子","兔子尾巴","佐乌",
                     "咕咕咕鸽咕咕","云雀","青鸟","仙鹤","长颈鹿"]

        hira = np.array(initdata.hiragana[:2]).flatten()
        rou = np.array(initdata.roumaji[:1]).flatten()
        kana = np.array(initdata.katakana[:1]).flatten()
        kana_range = np.append(hira,rou)
        kana_range = np.append(kana_range,kana)
        kana_range = kana_range.flatten()

        length_of_string = 3
        for i in range(100):
            message1 = random.choice(string.ascii_letters + string.digits + string.punctuation)
            message2 = np.random.choice(kana_range)
            print(message2)
            print(type(message2))
            messagelist = []
            messagelist.append(message1)
            messagelist.append(message2)
            message = np.random.choice(messagelist)
            name = np.random.choice(name_list)
            self.ex_data.append((name,message))
        print(len(self.ex_data))

    def run(self):
        for i in self.ex_data:
            time.sleep(1)
            self.testSignal.emit(i[0], i[1])
            print(f"{i[0]} {i[1]}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow(hiragana[:1])


    def connect_damakusource(type_class, main_window_object):
        # 实例化弹幕获取线程
        input_thread = type_class()
        # # 绑定更新弹幕函数
        input_thread.testSignal.connect(w.update_chat)
        input_thread.start()


    connect_damakusource(TestMainWindow, w)

    extra = {

        # Button colors
        'danger': '#dc3545',
        'warning': '#ffc107',
        'success': '#17a2b8',

        # Font
        'font_family': 'Microsoft YaHei',
        'font_size': '60px',
    }

    apply_stylesheet(app, theme='light_amber.xml',extra=extra)
    w.resize(1000, 800)
    w.move(200, 200)
    w.setWindowTitle('五十音答题')
    w.show()

    sys.exit(app.exec_())
