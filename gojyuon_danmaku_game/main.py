import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, \
    QScrollArea

from 五十音互动.gojyuon_danmaku_game.DANMAKU import *
from 五十音互动.gojyuon_danmaku_game.initdata import *
from 五十音互动.gojyuon_danmaku_game.initdata import shuffle, hiragana


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # 自定义资源位置！
        # 设置音频位置
        self.audio_dir = r"D:\Downloads\神夏分享\【符鱼整理】神夏一到三季资源各种分散\莫娘的歌.mp3"

        # 界面组件Widget初始化
        self.shuffleButton = QPushButton("抽")
        self.shuffleButton.setFont(QFont("Microsoft YaHei", 100))
        self.cancelButton = QPushButton("Cancel")
        self.questionLable = QLabel('')

        self.chatlabel = QLabel('')
        self.chatlabel_scroll_area = QScrollArea()
        self.player = QMediaPlayer()
        self.play_control = QPushButton()

        self.initUI()

        self.DANMAKU = DANMAKU()  # 实例化弹幕获取线程
        # 将自己的信号和Form2的接受函数绑定
        self.DANMAKU.testSignal.connect(self.update_chat)
        self.DANMAKU.start()

    def initUI(self):
        self.shuffleButton.clicked.connect(self.on_shuffle_click)
        self.questionLable.setFont(QFont("MS Mincho", 200, QFont.Bold))
        self.questionLable.setText("あ")

        self.play_control.setText('播放')
        self.play_control.clicked.connect(self.on_play_control_click)

        self.chatlabel.setText(blank_label_fill_str)
        self.chatlabel_scroll_area.setWidgetResizable(True)
        self.chatlabel_scroll_area.setWidget(self.chatlabel)
        self.chatlabel_scroll_area.verticalScrollBar().rangeChanged.connect(
            lambda: self.chatlabel_scroll_area.verticalScrollBar().setValue(
                self.chatlabel_scroll_area.verticalScrollBar().maximum()
            )
        )

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.questionLable, 0, 0, 1, 1)
        grid_layout.addWidget(self.shuffleButton, 0, 1, 1, 1)
        grid_layout.addWidget(self.play_control, 0, 2, 1, 1)
        self.player.setVolume(100)
        grid_layout.addWidget(self.chatlabel_scroll_area, 1, 1, 1, 1)

        # 设定第几行，占面积的比例
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 3)

        self.setLayout(grid_layout)

    @pyqtSlot()
    def on_shuffle_click(self):
        random_kana = shuffle(hiragana)
        self.questionLable.setText(random_kana)
        roumaji_char = get_roumaji(random_kana)
        self.change_audio(roumaji_char)

    def change_audio(self, roumaji_char):
        self.player.stop()
        self.audio_dir = self.get_audio_dir(roumaji_char)
        self.music_play_control()

    # TODO 更换音频
    def get_audio_dir(self, roumaji_char):
        return self.audio_dir

    def update_chat(self, message):
        messages = self.chatlabel.text() + "\n" + message
        print(messages)
        self.chatlabel.setText(messages)

    def on_play_control_click(self):
        self.music_play_control()
        self.timer_control()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.resize(1000, 800)
    w.move(200, 200)
    w.setWindowTitle('五十音答题')
    w.show()

    sys.exit(app.exec_())
