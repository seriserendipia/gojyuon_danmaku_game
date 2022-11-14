import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, \
    QScrollArea

from gojyuon_danmaku_game.danmaku import DANMAKU
from gojyuon_danmaku_game.QA_control import QAJudger, QA_question, QA_answer
from gojyuon_danmaku_game.initdata import shuffle, hiragana, get_roumaji, blank_label_fill_str
from gojyuon_danmaku_game.team_factory import TeamInfo


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # 自定义资源位置！

        # 界面组件Widget初始化
        self.shuffleButton = QPushButton("抽")
        self.shuffleButton.setFont(QFont("Microsoft YaHei", 100))
        self.cancelButton = QPushButton("Cancel")
        self.questionLable = QLabel('')

        self.chatlabel = QLabel(blank_label_fill_str)
        self.chatlabel_scroll_area = QScrollArea()
        self.scoring_label = QLabel(blank_label_fill_str)
        self.player = QMediaPlayer()
        self.play_control = QPushButton()

        self.initUI()

        self.DANMAKU = DANMAKU()  # 实例化弹幕获取线程
        # 将自己的信号和Form2的接受函数绑定
        self.DANMAKU.testSignal.connect(self.update_chat)
        self.DANMAKU.start()




    def initUI(self):
        self.team_info = TeamInfo()
        print(type(self.team_info.new_player_message_Signal))
        self.team_info.new_player_message_Signal.connect(self.update_scoring)

        self.shuffleButton.clicked.connect(self.on_shuffle_click)
        self.questionLable.setFont(QFont("MS Mincho", 200, QFont.Bold))
        self.questionLable.setText("あ")

        self.q_roumaji = "a"
        self.qa_judger = self.init_qa_judger()
        self.qa_judger.scoring_message_Signal.connect(self.update_scoring)

        # 设置音频位置
        self.audio_dir = self.get_audio_dir()
        self.play_control.setText('播放')
        self.play_control.clicked.connect(self.on_play_control_click)
        self.player.setVolume(100)

        self.chatlabel_scroll_area.setWidgetResizable(True)
        self.chatlabel_scroll_area.setWidget(self.chatlabel)
        self.chatlabel_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.chatlabel_scroll_area.verticalScrollBar().setValue(
                self.chatlabel_scroll_area.verticalScrollBar().maximum()
            )
        )

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.scoring_label,1,1,1,1)
        grid_layout.addWidget(self.shuffleButton, 0, 1, 1, 1)
        grid_layout.addWidget(self.play_control, 0, 2, 1, 1)
        grid_layout.addWidget(self.chatlabel_scroll_area, 1, 2
                              , 1, 1)

        # 设定第几行，占面积的比例
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 3)

        self.setLayout(grid_layout)

    def init_qa_judger(self):
        return QAJudger(QA_question(self.q_roumaji), self.team_info)

    @pyqtSlot()
    def on_shuffle_click(self):
        random_kana = shuffle(hiragana)
        self.questionLable.setText(random_kana)

        roumaji_char = get_roumaji(random_kana)
        self.change_audio(roumaji_char)

        self.qa_judger = self.init_qa_judger()

    def change_audio(self, roumaji_char):
        self.player.stop()
        self.audio_dir = self.get_audio_dir(roumaji_char)
        self.music_play_control()

    # TODO 更换音频
    def get_audio_dir(self, roumaji_char):
        audio_dir = fr"音声素材/kana50on_{roumaji_char}.mp3"
        return audio_dir

    def update_chat(self, message,nickname):
        message_format = f'>> {message}：{nickname}'
        messages = self.chatlabel.text() + "\n" + message_format
        print(message_format)
        self.chatlabel.setText(messages)
        self.qa_judger.answer_process(QA_answer(raw_answer=message,q_roumaji=self.qa_judger.question.q_roumaji,nickname=nickname))

    def update_scoring(self, message):
        messages = self.scoring_label.text() + "\n" + message
        self.scoring_label.setText(messages)

    def on_play_control_click(self):
        self.music_play_control()
        self.timer_control()
        self.scoring_control()

    def scoring_control(self):
        pass

    def music_play_control(self):
        # 判断是否是暂停状态
        if self.player.state() == QMediaPlayer.State.PausedState:
            self.play_music()
        # 判断是否是播放状态,是就暂停
        elif self.player.state() == QMediaPlayer.State.PlayingState:
            self.pause_music()
        # 初始化音频内容
        else:
            self.init_play_content()

    def init_play_content(self):
        audio_dir = self.audio_dir
        self.media_content = QMediaContent(QUrl.fromLocalFile(audio_dir))  # 2
        self.player.setMedia(self.media_content)

    def play_music(self):
        # 更改播放器为播放状态
        self.player.play()
        # 更改播放按钮为播放图片
        # self.play_control.setIcon(QIcon('D:\Program Files (x86)\Python\Myplayer\image\播放.png'))
        # 设置提示信息为播放
        self.play_control.setText('播放')

    def pause_music(self):
        # 更改播放器为暂停状态
        self.player.pause()
        # 更改播放按钮的图片为暂停图片
        # self.play_control.setIcon(QIcon('D:\Program Files (x86)\Python\Myplayer\image\暂停.png'))
        # 设置提示信息为暂停
        self.play_control.setText('暂停')

    # TODO 计时器暂停
    def timer_control(self):
        pass

    def update_scoreing_label(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.resize(1000, 800)
    w.move(200, 200)
    w.setWindowTitle('五十音答题')
    w.show()

    sys.exit(app.exec_())
