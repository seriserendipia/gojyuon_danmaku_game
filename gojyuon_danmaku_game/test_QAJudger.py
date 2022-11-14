from unittest import TestCase

from gojyuon_danmaku_game.QA_control import QA_answer


class TestQAJudger(TestCase):
    def test_wash_raw_answer(self):
        self.assertEqual(QA_answer("sdfghj","vbd").answer,"sdf")
        self.assertEqual(QA_answer("aaaaa","i").answer,"a")
        self.assertEqual(QA_answer("あ","fghvsdzk").answer,"あ")
        self.assertEqual(QA_answer("１２３４４５５","fvgbhnjm").answer,"１")
