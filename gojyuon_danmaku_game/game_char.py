import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTransform
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, \
    QScrollArea, QListWidget, QListWidgetItem, QSizePolicy, QGroupBox, QHBoxLayout


from gojyuon_danmaku_game.QA_control import ListeningQAJudger, QA_question, QA_answer, SignatureQAJudger
from gojyuon_danmaku_game.danmaku import DANMAKU
from gojyuon_danmaku_game.initdata import shuffle, hiragana, get_roumaji, blank_label_fill_str, get_hiragana, katakana
from gojyuon_danmaku_game.team import TeamInfo
from gojyuon_danmaku_game.gendata_test import TestDataGeneratorThread


class SignatureGameWindow(QWidget):
    input_thread_properly_stop_signal = QtCore.pyqtSignal()

    def __init__(self,kana_range):
        super().__init__()
        #指定随机范围
        self.kana_range = kana_range

        # 界面组件Widget初始化
        self.shuffleButton = QPushButton()

        self.play_control = QPushButton("开始")
        self.play_control.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.chatlabel = QLabel(blank_label_fill_str)
        self.chatlabel_scroll_area = QScrollArea()
        self.chatlabel.setWordWrap(True)
        self.chatlabel_groupbox = QGroupBox("实时弹幕")
        self.chat_layout = QHBoxLayout()
        self.chat_layout.addWidget(self.chatlabel_scroll_area)
        self.chatlabel_groupbox.setLayout(self.chat_layout)

        self.scoring_label = QLabel(blank_label_fill_str)
        self.scoring_label_scroll_area = QScrollArea()
        self.scoring_label.setWordWrap(True)
        self.scoring_label_groupbox = QGroupBox("游戏记录")
        self.scoring_layout = QHBoxLayout()
        self.scoring_layout.addWidget(self.scoring_label_scroll_area)
        self.scoring_label_groupbox.setLayout(self.scoring_layout)

        self.question_label = QLabel()

        self.red_team_member_listview = QTeamListWidget("红")
        self.red_team_member_groupbox = QGroupBox("红队队员")
        self.red_team_member_layout = QHBoxLayout()
        self.red_team_member_layout.addWidget(self.red_team_member_listview)
        self.red_team_member_groupbox.setLayout(self.red_team_member_layout)

        self.blue_team_member_listview = QTeamListWidget("蓝")
        self.blue_team_member_groupbox = QGroupBox("蓝队队员")
        self.blue_team_member_layout = QHBoxLayout()
        self.blue_team_member_layout.addWidget(self.blue_team_member_listview)
        self.blue_team_member_groupbox.setLayout(self.blue_team_member_layout)

        self.red_team_score_label = QLabel("红队\n得分：0")
        self.red_team_score_label.setFont(QFont("Microsoft YaHei", 30))
        self.red_team_score_label.setProperty('class', 'danger')
        self.blue_team_score_label = QLabel("蓝队\n得分：0")
        self.blue_team_score_label.setFont(QFont("Microsoft YaHei", 30))
        self.blue_team_score_label.setProperty('class', 'success')

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.play_icon = QIcon(r"..\res\drawable\播放.png")
        self.pause_icon = QIcon(r"..\res\drawable\暂停.png")

        self.initUI()



    def initUI(self):
        self.team_info = TeamInfo()
        self.team_info.new_player_message_Signal.connect(self.update_scoring)
        self.team_info.refresh_team_list_Signal.connect(self.update_team_list)

        self.shuffleButton.clicked.connect(self.on_shuffle_click)
        self.play_control.clicked.connect(self.on_play_control_click)

        # 初始化第一题，自定义资源位置！
        random_kana = "あ"
        self.init_new_question(random_kana)



        self.player.setVolume(100)

        self.chatlabel_scroll_area.setWidgetResizable(True)
        self.chatlabel_scroll_area.setWidget(self.chatlabel)
        self.chatlabel_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.chatlabel_scroll_area.verticalScrollBar().setValue(
                self.chatlabel_scroll_area.verticalScrollBar().maximum()
            )
        )

        self.scoring_label_scroll_area.setWidgetResizable(True)
        self.scoring_label_scroll_area.setWidget(self.scoring_label)
        self.scoring_label_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.scoring_label_scroll_area.verticalScrollBar().setValue(
                self.scoring_label_scroll_area.verticalScrollBar().maximum()
            )
        )

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.red_team_score_label,0,0,1,1)
        self.grid_layout.addWidget(self.blue_team_score_label,0,3,1,1)
        self.grid_layout.addWidget(self.question_label,0,1,1,2, alignment=Qt.AlignCenter)
        self.grid_layout.addWidget(self.shuffleButton, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.play_control, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.scoring_label_groupbox,2,1,1,1)
        self.grid_layout.addWidget(self.chatlabel_groupbox, 2, 2, 1, 1)
        self.grid_layout.addWidget(self.red_team_member_groupbox,1,0,3,1)
        self.grid_layout.addWidget(self.blue_team_member_groupbox,1,3,3,1)

        # 设定第几行，占面积的比例
        self.grid_layout.setRowStretch(0, 2)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(2, 2)

        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 2)
        self.grid_layout.setColumnStretch(2, 2)
        self.grid_layout.setColumnStretch(3, 1)


        self.shuffle_pix = QPixmap(r"..\res\drawable\随机数生成-选中.png")
        self.shuffleButton.setIcon(QIcon(self.shuffle_pix))
        self.shuffleButton.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.shuffleButton.setIconSize(QSize(128, 128))

        self.play_control.setIcon(self.play_icon)
        self.play_control.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.play_control.setIconSize(QSize(128, 128))

        self.setLayout(self.grid_layout)

    def on_play_control_click(self):
        self.music_play_control()
        self.timer_control()
        self.scoring_control()

    def music_play_control(self):
        # 判断是否是暂停状态
        if self.play_control.text() == "暂停中":
            self.play()
        # 判断是否是播放状态,是就暂停
        elif self.play_control.text() == "播放中":
            self.pause()
        # 初始化音频内容
        else:
            self.play()



    def init_signature_qa_judger(self):
        return SignatureQAJudger(QA_question(self.q_roumaji,self.kana), self.team_info)



    def on_shuffle_click(self):
        transform = QTransform()  ##需要用到pyqt5中QTransform函数
        transform.rotate(90)  ##设置旋转角度——顺时针旋转90°
        self.shuffle_pix = self.shuffle_pix.transformed(transform)  ##对image进行旋转
        self.shuffleButton.setIcon(QIcon(self.shuffle_pix))
        self.shuffleButton.setIconSize(QSize(128, 128))
        print("换题啦！！！！！！！！！")
        random_kana = shuffle(self.kana_range)
        self.init_new_question(random_kana)
        self.update_scoring("---------题目刷新---------------")

    def init_new_question(self, random_kana):
        self.kana = random_kana
        self.q_roumaji = get_roumaji(random_kana)
        self.question_label.setText(random_kana)
        self.question_label.setFont(QFont("MS Mincho",120))
        self.signature_qa_judger = self.init_signature_qa_judger()
        self.signature_qa_judger.scoring_message_Signal.connect(self.update_scoring)

    def play(self):
        print("开始播放了！！！！！！！！！！！！！！！！！！！")
        # 更改播放按钮为播放图片
        self.play_control.setIcon(self.play_icon)
        # 设置提示信息为播放
        self.play_control.setText("播放中")


    def pause(self):
        print("暂停了！！！！！！！！！！！！！！")
        # 更改播放按钮的图片为暂停图片
        self.play_control.setIcon(self.pause_icon)
        # 设置提示信息为暂停
        self.play_control.setText('暂停中')
        print("游戏状态为：",self.play_control.text())
        self.play_control.repaint()

    # TODO 计时器暂停
    def timer_control(self):
        pass

    #TODO 记分暂停
    def scoring_control(self):
        print("判断状态中————————",self.play_control.text())
        if self.play_control.text() == '暂停中':
            self.signature_qa_judger.CAN_SCORE = False
            self.update_scoring("--------暂停中------------")
        elif self.play_control.text() == '播放中':
            self.signature_qa_judger.CAN_SCORE = True

    def update_chat(self, nickname, message):
        message_format = f'>> {nickname}：{message}'
        messages = self.chatlabel.text() + "\n" + message_format + "\n"
        print(message_format)
        self.chatlabel.setText(messages)
        self.signature_qa_judger.juder(QA_answer(raw_answer=message, q_roumaji=self.q_roumaji, nickname=nickname))

    def update_scoring(self, message):
        messages = self.scoring_label.text() + "\n" + message
        self.scoring_label.setText(messages)
        print(message)
        self.update_team_score()

    def update_team_score(self):
        self.red_team_score_label.setText("红队\n得分：" + str(self.team_info.team_red.score))
        self.blue_team_score_label.setText("蓝队\n得分：" + str(self.team_info.team_blue.score))

    def update_team_list(self,team_flag,nickname):
        if team_flag == self.red_team_member_listview.team_flag:
            self.red_team_member_listview.insertItem(0,QListWidgetItem(nickname))
        elif team_flag == self.blue_team_member_listview.team_flag:
            self.blue_team_member_listview.insertItem(0,QListWidgetItem(nickname))

    def closeEvent(self, event) -> None:
        self.input_thread_properly_stop_signal.emit()
        super(SignatureGameWindow, self).closeEvent()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = SignatureGameWindow(katakana[:3])

    # 实例化弹幕获取线程
    input_thread = DANMAKU()
    # # 绑定更新弹幕函数
    input_thread.danmaku_message_signal.connect(w.update_chat)
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
