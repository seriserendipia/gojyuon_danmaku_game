import unittest

from gojyuon_danmaku_game.QA_control import *


class MyTestCase(unittest.TestCase):
    def test_is_answer_right(self):
        answer, q_roumaji = "a","a"
        judgment= ListeningQAJudger().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment,True)

        answer, q_roumaji = "a", "あ"
        judgment = ListeningQAJudger().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, True)

        answer, q_roumaji = "a", "ア"
        judgment = ListeningQAJudger().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, True)

        answer, q_roumaji = "a", "％"
        judgment = ListeningQAJudger().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, False)

        answer, q_roumaji = "a", "い"
        judgment = ListeningQAJudger().is_answer_right(answer, q_roumaji)
        self.assertEqual(judgment, False)

    def test_gen_scoring_message(self):
        nickname = "猫猫"
        isFirstBlood = True
        ANSWERTYPE = 0
        hasFirstRightAnswer = True
        score = ListeningQAJudger().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = ListeningQAJudger().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

        nickname = "狗狗"
        isFirstBlood = False
        ANSWERTYPE = 3
        hasFirstRightAnswer = False
        score = ListeningQAJudger().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = ListeningQAJudger().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

        nickname = "蓝鲸鱼"
        isFirstBlood = True
        ANSWERTYPE = 2
        hasFirstRightAnswer = True
        score = ListeningQAJudger().gen_score(hasFirstRightAnswer, ANSWERTYPE)
        message = ListeningQAJudger().gen_scoring_message(nickname, isFirstBlood, ANSWERTYPE, score)
        print(message)

if __name__ == '__main__':
    unittest.main()
