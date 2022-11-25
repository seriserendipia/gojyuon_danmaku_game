from abc import abstractmethod

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, \
    QScrollArea, QListWidget, QListWidgetItem, QSizePolicy, QGroupBox, QHBoxLayout

from customize_config import play_tip, pause_tip
from gojyuon_danmaku_game.QA_control import QA_answer
from gojyuon_danmaku_game.initdata import shuffle, get_roumaji, blank_label_fill_str
from gojyuon_danmaku_game.team import TeamInfo


class QTeamListWidget(QListWidget):
    def __init__(self, team_flag):
        super(QTeamListWidget, self).__init__()
        self.team_flag = team_flag


class BaseGUI(QWidget):
    input_thread_properly_stop_signal = QtCore.pyqtSignal()

    def __init__(self, kana_range):
        super().__init__()
        # 指定随机范围
        self.kana_range = kana_range

        # 界面组件Widget初始化
        self.shuffleButton = QPushButton()

        self.play_control = QPushButton("开始")
        self.play_control.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.chatlabel = QLabel(blank_label_fill_str)
        self.chatlabel.setWordWrap(True)
        self.chatlabel_scroll_area = QScrollArea()
        self.chatlabel_scroll_area.setWidget(self.chatlabel)
        self.chatlabel_groupbox = QGroupBox("实时弹幕")
        self.chat_layout = QHBoxLayout()
        self.chat_layout.addWidget(self.chatlabel_scroll_area)
        self.chatlabel_groupbox.setLayout(self.chat_layout)

        self.scoring_label = QLabel(blank_label_fill_str)
        self.scoring_label.setWordWrap(True)
        self.scoring_label_scroll_area = QScrollArea()
        self.scoring_label_scroll_area.setWidget(self.scoring_label)
        self.scoring_label_groupbox = QGroupBox("游戏记录")
        self.scoring_layout = QHBoxLayout()
        self.scoring_layout.addWidget(self.scoring_label_scroll_area)
        self.scoring_label_groupbox.setLayout(self.scoring_layout)

        self.middle_label = QLabel()

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

        self.play_icon = QIcon(r"..\res\drawable\播放.png")
        self.pause_icon = QIcon(r"..\res\drawable\暂停.png")

        self.initUI()

    def initUI(self):
        self.team_info = TeamInfo()
        self.team_info.new_player_message_Signal.connect(self.update_scoring)
        self.team_info.refresh_team_list_Signal.connect(self.update_team_list)

        self.shuffleButton.clicked.connect(self.on_shuffle_click)
        self.play_control.clicked.connect(self.on_play_control_click)

        # 初始化第一题
        self.init_new_question("a")

        self.chatlabel_scroll_area.setWidgetResizable(True)
        self.chatlabel_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.chatlabel_scroll_area.verticalScrollBar().setValue(
                self.chatlabel_scroll_area.verticalScrollBar().maximum()
            )
        )

        self.scoring_label_scroll_area.setWidgetResizable(True)
        self.scoring_label_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.scoring_label_scroll_area.verticalScrollBar().setValue(
                self.scoring_label_scroll_area.verticalScrollBar().maximum()
            )
        )

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.red_team_score_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.blue_team_score_label, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.middle_label, 0, 1, 1, 2, alignment=Qt.AlignCenter)
        self.grid_layout.addWidget(self.shuffleButton, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.play_control, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.scoring_label_groupbox, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.chatlabel_groupbox, 2, 2, 1, 1)
        self.grid_layout.addWidget(self.red_team_member_groupbox, 1, 0, 3, 1)
        self.grid_layout.addWidget(self.blue_team_member_groupbox, 1, 3, 3, 1)

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
        self.shuffleButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.shuffleButton.setIconSize(QSize(128, 128))

        self.play_control.setIcon(self.play_icon)
        self.play_control.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.play_control.setIconSize(QSize(128, 128))

        self.setLayout(self.grid_layout)

    @abstractmethod
    def init_qa_judger(self):
        pass

    def on_shuffle_click(self):
        transform = QTransform()  ##需要用到pyqt5中QTransform函数
        transform.rotate(90)  ##设置旋转角度——顺时针旋转90°
        self.shuffle_pix = self.shuffle_pix.transformed(transform)  ##对image进行旋转
        self.shuffleButton.setIcon(QIcon(self.shuffle_pix))
        self.shuffleButton.setIconSize(QSize(128, 128))
        random_kana = shuffle(self.kana_range)
        random_roumaji_char = get_roumaji(random_kana)
        self.init_new_question(random_roumaji_char)
        print("---------题目刷新---------------")
        self.update_scoring("---------题目刷新---------------")

    def init_new_question(self, random_roumaji_char):
        self.q_roumaji = random_roumaji_char
        self.qa_judger = self.init_qa_judger()
        self.qa_judger.scoring_message_Signal.connect(self.update_scoring)

    def on_play_control_click(self):
        self.set_play_status()
        self.timer_control()
        self.scoring_control()

    def set_play_status(self):
        icon = self.play_icon
        tip = play_tip
        self.set_play_control_button_appearance(icon, tip)

    def set_pause_status(self):
        icon = self.pause_icon
        tip = pause_tip
        self.set_play_control_button_appearance(icon, tip)

    def set_play_control_button_appearance(self, icon, tip):
        # 更改播放按钮的图片
        self.play_control.setIcon(icon)
        # 设置提示信息
        self.play_control.setToolTip(tip)
        self.play_control.repaint()
        print(f"-----------{tip}----------------")
        self.update_scoring(f"--------{tip}------------")

    # TODO 计时器暂停
    def timer_control(self):
        pass

    def scoring_control(self):
        if self.play_control.toolTip() == pause_tip:
            self.qa_judger.CAN_SCORE = False
        elif self.play_control.toolTip() == play_tip:
            self.qa_judger.CAN_SCORE = True

    def update_chat(self, nickname, message):
        message_format = f'>> {nickname}：{message}'
        messages = self.chatlabel.text() + "\n" + message_format + "\n"
        print(message_format)
        self.chatlabel.setText(messages)
        self.qa_judger.juder(QA_answer(raw_answer=message, q_roumaji=self.q_roumaji, nickname=nickname))

    def update_scoring(self, message):
        messages = self.scoring_label.text() + "\n" + message
        self.scoring_label.setText(messages)
        print(message)
        self.update_team_score()

    def update_team_score(self):
        self.red_team_score_label.setText("红队\n得分：" + str(self.team_info.team_red.score))
        self.blue_team_score_label.setText("蓝队\n得分：" + str(self.team_info.team_blue.score))

    def update_team_list(self, team_flag, nickname):
        if team_flag == self.red_team_member_listview.team_flag:
            self.red_team_member_listview.insertItem(0, QListWidgetItem(nickname))
        elif team_flag == self.blue_team_member_listview.team_flag:
            self.blue_team_member_listview.insertItem(0, QListWidgetItem(nickname))

    def closeEvent(self, event) -> None:
        self.input_thread_properly_stop_signal.emit()
        super(BaseGUI, self).closeEvent(event)
