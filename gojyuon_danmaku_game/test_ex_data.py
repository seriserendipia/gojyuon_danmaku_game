import random
import string
import sys
import time

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication


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
            messagelist = []
            messagelist.append(message1)
            messagelist.append(message2)
            message = np.random.choice(messagelist)
            name = np.random.choice(name_list)
            self.ex_data.append((name,message))

    def run(self):
        for i in self.ex_data:
            time.sleep(2)
            self.testSignal.emit(i[0], i[1])
            print(f"{i[0]} {i[1]}")

    def properly_stop(self):
        print("结束进程")
        self.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow(hiragana[:1])

    # 实例化弹幕获取线程
    input_thread = TestMainWindow()
    # # 绑定更新弹幕函数
    input_thread.testSignal.connect(w.update_chat)
    input_thread.start()

    stylesheetdir = "../res/drawable/my_stylesheet.qss"
    with open(stylesheetdir, "r+") as fh:
        stylesheet = fh.read()
        w.setStyleSheet(stylesheet)
        try:
            app.setStyleSheet(stylesheet)
        except:
            app.style_sheet = stylesheet

    w.resize(1000, 800)
    w.move(200, 200)
    w.setWindowTitle('五十音弹幕游戏')
    w.show()

    sys.exit(app.exec_())
