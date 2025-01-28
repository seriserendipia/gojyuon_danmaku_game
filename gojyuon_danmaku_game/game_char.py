import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from gojyuon_danmaku_game.QA_control import QA_question, CharQAJudger
from gojyuon_danmaku_game.danmaku import DANMAKU
from gojyuon_danmaku_game.game_basegui import GameBaseGUI
from gojyuon_danmaku_game.initdata import katakana, hiragana


class CharGame(GameBaseGUI):

    def initUI(self):
        super(CharGame, self).initUI()

    def init_qa_judger(self):
        return CharQAJudger(QA_question(self.q_roumaji, self.q_char), self.team_info)

    def init_new_question(self, random_kana):
        super(CharGame, self).init_new_question(random_kana)
        self.middle_label.setText(random_kana)
        self.middle_label.setFont(QFont("MS Mincho", 120))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = CharGame(hiragana[:-2])

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
