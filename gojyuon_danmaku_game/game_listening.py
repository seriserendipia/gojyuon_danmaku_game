import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication

from gojyuon_danmaku_game.QA_control import ListeningQAJudger, QA_question
from gojyuon_danmaku_game.danmaku import DANMAKU
from gojyuon_danmaku_game.game_basegui import GameBaseGUI
from gojyuon_danmaku_game.initdata import hiragana


class ListeningGame(GameBaseGUI):

    def __init__(self, char_range):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        super(ListeningGame, self).__init__(char_range)

    def initUI(self):
        super(ListeningGame, self).initUI()
        self.player.setVolume(100)
        rule_pic = QPixmap(r"..\res\drawable\游戏规则（不带倒计时版）.png")
        self.middle_label.setPixmap(rule_pic)

    def init_qa_judger(self):
        return ListeningQAJudger(QA_question(self.q_roumaji,self.q_char), self.team_info)

    def init_new_question(self, random_char):
        super(ListeningGame, self).init_new_question(random_char)
        self.change_audio()

    def change_audio(self):
        self.player.stop()
        self.audio_dir = self.get_audio_dir()
        self.music_play_control()

    def get_audio_dir(self):
        roumaji = self.q_roumaji
        audio_dir = rf"..\res\音声素材\kana50on_{roumaji}.mp3"
        return audio_dir

    def on_play_control_click(self):
        super(ListeningGame, self).on_play_control_click()
        self.music_play_control()

    def music_play_control(self):
        # 判断是否是暂停状态
        if self.player.state() == QMediaPlayer.State.PausedState:
            self.play_music()
        # 判断是否是播放状态,是就暂停
        elif self.player.state() == QMediaPlayer.State.PlayingState:
            self.pause_music()
        # 初始化音频内容
        else:
            print("初始化音频！！！！！！！！！")
            self.init_play_content()
            self.play_music()

    def init_play_content(self):
        audio_dir = self.audio_dir
        print("音频路径：", audio_dir)
        self.playlist.clear()

        self.media_content = QMediaContent(QUrl.fromLocalFile(audio_dir))
        self.playlist.addMedia(self.media_content)
        # TODO 减低频率，添加空白音频
        blank_media_content = QMediaContent(QUrl.fromLocalFile(r"..\res\音声素材\empty_voice.m4a"))
        self.playlist.addMedia(blank_media_content)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    def play_music(self):
        self.player.play()

    def pause_music(self):
        self.player.pause()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = ListeningGame(hiragana[3:4])

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
