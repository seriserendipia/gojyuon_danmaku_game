import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from gojyuon_danmaku_game.initdata import hiragana, katakana, \
    roumaji, get_roumaji, get_hiragana
from gojyuon_danmaku_game.team import TeamInfo


class QA_question():

    def __init__(self, q_roumaji, *kana):
        self.q_roumaji = q_roumaji
        if len(kana) == 0:
            self.q_kana = get_hiragana(self.q_roumaji)
        else:
            self.q_kana = kana[0]
        self.hasFirstRightAnswer = False


class QA_answer():
    def __init__(self,raw_answer,q_roumaji,nickname):
        self.q_roumaji = q_roumaji
        self.raw_answer = raw_answer
        self.answer = self.wash_raw_answer()
        self.nickname = nickname

    def wash_raw_answer(self):
        raw_answer = self.raw_answer
        answer = raw_answer.strip()
        if len(answer) > len(self.q_roumaji) or len(answer) > 3:
            answer = answer[:max(3,len(self.q_roumaji))]
        answer = answer.lower()
        for i in range(1,len(answer)):
            if answer.encode( 'UTF-8' ).isalpha() == True:
                pass
            else:
                answer = answer[:i]
        return answer


# %%
class ListeningQAJudger(QThread):
    scoring_message_Signal = QtCore.pyqtSignal(str)

    # 得分数值策划
    FIRSTBLOODBONUSSCORE = 2
    BASIC_SCORE = 1
    ROUMAJIBOUNUS = 0
    HIRAGANABONUS = 2
    KATAGANABONUS = 3


    def __init__(self, question:QA_question,team_info:TeamInfo):
        super(ListeningQAJudger, self).__init__()
        self.question = question
        self.team_info = team_info
        self.CAN_SCORE = True

    def juder(self, answerobj:QA_answer):
        message = "\n"
        try:
            if self.CAN_SCORE == True:
                message = self.answer_process(answerobj)
            else:
                pass
        except Exception as e:
            message = f"{str(e)}"
            print("err:",traceback.print_exc())
        finally:
            self.show_message(message)

    def is_answer_right(self):
        try:
            if get_roumaji(self.answer) == get_roumaji(self.question.q_roumaji):
                return True
            else:
                return False
        except Exception as e:
            if hasattr(e, 'message'):
                print("答案错误",e.message)
            else:
                print("答案错误",e)
            return False
    

    def first_blood_message(self):
        if not self.question.hasFirstRightAnswer:
            return f"拿到首杀 + {self.FIRSTBLOODBONUSSCORE} 分；"
        else:
            return ""
    
    
    def get_answer_type(self):
        answer = self.answer
        # -1 表示错误答案
        ANSWERTYPE = -1
        if answer in hiragana:
            ANSWERTYPE = self.HIRAGANABONUS
        elif answer in katakana:
            ANSWERTYPE = self.KATAGANABONUS
        elif answer in roumaji:
            ANSWERTYPE = self.ROUMAJIBOUNUS
        if ANSWERTYPE == -1:
            raise Exception(f"回答‘{answer}‘不在清音的平假名、片假名、罗马音中")
        return ANSWERTYPE
    
    
    def answer_type_bonus_message(self):
        ANSWERTYPE = self.ANSWERTYPE
        if ANSWERTYPE == self.ROUMAJIBOUNUS:
            answer_type_bonus_str = f""
        elif ANSWERTYPE == self.HIRAGANABONUS:
            answer_type_bonus_str = f"使用平假名回答 + {self.HIRAGANABONUS} 分；"
        elif ANSWERTYPE == self.KATAGANABONUS:
            answer_type_bonus_str = f"使用片假名回答 + {self.KATAGANABONUS} 分；"
        else:
            raise Exception("ANSWERTYPE out of range")
        return answer_type_bonus_str
    
    
    def gen_score(self):
        hasFirstRightAnswer = self.question.hasFirstRightAnswer
        ANSWERTYPE = self.ANSWERTYPE
        score = self.BASIC_SCORE
        if hasFirstRightAnswer == False:
            score += self.FIRSTBLOODBONUSSCORE
        score += ANSWERTYPE
        return score
    
    
    def gen_scoring_message(self):
        nickname= self.answerobj.nickname
        hasFirstRightAnswer = self.question.hasFirstRightAnswer
        ANSWERTYPE = self.ANSWERTYPE
        message = "".join([
            nickname,
            f" 回答正确 + {self.BASIC_SCORE} 分；",
            self.first_blood_message(),
            self.answer_type_bonus_message()])
        return message
    
    
    def answer_process(self,answerobj:QA_answer):
        nickname = answerobj.nickname
        team_flag = self.team_info.get_player_assign_team(nickname)

        self.answerobj = answerobj
        self.answer = answerobj.answer
        self.ANSWERTYPE = self.get_answer_type()

        if self.is_answer_right():
            score = self.gen_score()
            message = self.gen_scoring_message()
            self.add_score(score,team_flag)
            self.question.hasFirstRightAnswer = True
        else:
            message = f"{self.answer}不是正确答案哦"
        return message

    def add_score(self, score,team_flag):
        self.team_info.add_score(score,team_flag)

    def show_message(self, message):
        self.scoring_message_Signal.emit(message)


class SignatureQAJudger(ListeningQAJudger):

    def is_answer_right(self):
        try:
            if self.answer == self.question.q_kana:
                raise Exception("{self.answer}是题面哦")
            else:
                if get_roumaji(self.answer) == get_roumaji(self.question.q_kana):
                    return True
                else:
                    return False
        except Exception as e:
            if hasattr(e, 'message'):
                print("答案错误",e.message)
            else:
                print("答案错误",e)
            return False
