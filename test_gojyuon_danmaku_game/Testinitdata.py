import unittest

from 五十音互动.gojyuon_danmaku_game.QA import *


class MyTestCase(unittest.TestCase):
    def test_is_answer_right(self):
        answer, q_roumaji = "a","a"
        judgment= QA().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment,True)

        answer, q_roumaji = "a", "あ"
        judgment = QA().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, True)

        answer, q_roumaji = "a", "ア"
        judgment = QA().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, True)

        answer, q_roumaji = "a", "％"
        judgment = QA().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, False)

        answer, q_roumaji = "a", "い"
        judgment = QA().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, False)

    def test_gen_scoring_message(self):
        nickname = "猫猫"
        isFirstBlood = True
        ANSWERTYPE = 0
        hasFirstRightAnswer = True
        score = QA().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = QA().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

        nickname = "狗狗"
        isFirstBlood = False
        ANSWERTYPE = 3
        hasFirstRightAnswer = False
        score = QA().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = QA().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

        nickname = "蓝鲸鱼"
        isFirstBlood = True
        ANSWERTYPE = 2
        hasFirstRightAnswer = True
        score = QA().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = QA().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

if __name__ == '__main__':
    unittest.main()
