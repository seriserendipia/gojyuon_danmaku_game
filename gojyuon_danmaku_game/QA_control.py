import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from gojyuon_danmaku_game.initdata import hiragana, katakana, \
    roumaji, get_roumaji
from gojyuon_danmaku_game.team_factory import TeamInfo


class QA_question():

    def __init__(self,q_roumaji):
        self.q_roumaji = q_roumaji
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
        if len(answer) > len(self.q_roumaji):
            answer = answer[:len(self.q_roumaji)]
        answer = answer.lower()
        if answer.encode( 'UTF-8' ).isalpha() == True:
            pass
        else:
            answer = answer[:1]
        return answer


# %%
class QAJudger(QThread):
    scoring_message_Signal = QtCore.pyqtSignal(str)

    # 得分数值策划
    FIRSTBLOODBONUSSCORE = 2
    BASIC_SCORE = 1
    ROUMAJIBOUNUS = 0
    HIRAGANABONUS = 2
    KATAGANABONUS = 3


    def __init__(self, question:QA_question,team_info:TeamInfo):
        super(QAJudger,self).__init__()
        self.question = question
        self.team_info = team_info
        self.CAN_SCORE = True

    def is_answer_right(self):
        try:
            if get_roumaji(self.answer) == get_roumaji(self.question.q_roumaji):
                return True
            else:
                print(f"答案错误 \"{self.answer}\" 被作为答案尝试过了")
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
        hasFirstRightAnswer, ANSWERTYPE = self.question.hasFirstRightAnswer,self.answer
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
            self.first_blood_message(hasFirstRightAnswer),
            self.answer_type_bonus_message(ANSWERTYPE)])
        return message
    
    
    def answer_process(self,answerobj:QA_answer):
        if self.CAN_SCORE == True:
            try:
                self.answerobj = answerobj
                self.answer = answerobj.answer
                self.ANSWERTYPE = self.get_answer_type()

                if self.is_answer_right():
                    score = self.gen_score()
                    message = self.gen_scoring_message()


                    self.add_score(score)
                    self.question.hasFirstRightAnswer = True
            except Exception as e:
                message = f"不能识别的答案:{str(e)}"


            finally:
                self.show_message(message)

    def add_score(self, score):
        nickname = self.answerobj.nickname
        team_flag = self.team_info.get_team_flag(nickname)
        self.team_info.add_score(score,team_flag)

    def show_message(self, message):
        self.scoring_message_Signal.emit(message)
