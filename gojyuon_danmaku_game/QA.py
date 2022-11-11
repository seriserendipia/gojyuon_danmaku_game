import traceback

from gojyuon_danmaku_game.initdata import get_roumaji, hiragana, katakana, \
    roumaji

# %%
class QA:
    # 得分数值策划
    FIRSTBLOODBONUSSCORE = 2
    BASIC_SCORE = 1
    ROUMAJIBOUNUS = 0
    HIRAGANABONUS = 2
    KATAGANABONUS = 3

    def __init__(self):
        self.hasFirstRightAnswer = False

    def wash_raw_answer(self,raw_answer:str):
        raw_answer = raw_answer.strip()




    def is_answer_right(self,answer, q_roumaji):
        try:
            if get_roumaji(answer) == get_roumaji(q_roumaji):
                return True
            else:
                print(f"答案错误 \"{answer}\" 被作为答案尝试过了")
                return False
        except Exception as e:
            if hasattr(e, 'message'):
                print("答案错误",e.message)
            else:
                print("答案错误",e)
            return False
    

    def first_blood_message(self, hasFirstRightAnswer):
        if not hasFirstRightAnswer:
            return f"拿到首杀 + {self.FIRSTBLOODBONUSSCORE} 分；"
        else:
            return ""
    
    
    def get_answer_type(self,answer):
        # -1 表示错误答案
        ANSWERTYPE = -1
        if answer in hiragana:
            ANSWERTYPE = self.HIRAGANABONUS
        elif answer in katakana:
            ANSWERTYPE = self.KATAGANABONUS
        elif answer in roumaji:
            ANSWERTYPE = self.ROUMAJIBOUNUS
        if ANSWERTYPE == -1:
            raise Exception("答案正确却不在平假名、片假名、罗马音中")
        return ANSWERTYPE
    
    
    def answer_type_bonus_message(self,ANSWERTYPE):
        if ANSWERTYPE == self.ROUMAJIBOUNUS:
            answer_type_bonus_str = f""
        elif ANSWERTYPE == self.HIRAGANABONUS:
            answer_type_bonus_str = f"使用平假名回答 + {self.HIRAGANABONUS} 分；"
        elif ANSWERTYPE == self.KATAGANABONUS:
            answer_type_bonus_str = f"使用片假名回答 + {self.KATAGANABONUS} 分；" \
                                    f""
        else:
            raise Exception("ANSWERTYPE out of range")
        return answer_type_bonus_str
    
    
    def gen_score(self, hasFirstRightAnswer, ANSWERTYPE):
        score = self.BASIC_SCORE
        if hasFirstRightAnswer == False:
            score += self.FIRSTBLOODBONUSSCORE
        score += ANSWERTYPE
        return score
    
    
    def gen_scoring_message(self, nickname: str, hasFirstRightAnswer: bool, ANSWERTYPE, score):
        score
        message = "".join([
            nickname,
            f" 回答正确 + {self.BASIC_SCORE} 分；",
            self.first_blood_message(hasFirstRightAnswer),
            self.answer_type_bonus_message(ANSWERTYPE)])
        return message
    
    
    def answer_process(self, nickname, answer, q_roumaji):
        try:
            if self.is_answer_right(answer, q_roumaji):
                ANSWERTYPE = self.get_answer_type(answer)
                score = self.gen_score(self.hasFirstRightAnswer, ANSWERTYPE)
                message = self.gen_scoring_message(nickname, self.hasFirstRightAnswer, ANSWERTYPE, score)
                print(message)

                self.add_score(nickname,score)
                self.show_message(message)

                self.hasFirstRightAnswer = True
        except Exception as e:
            print("不能识别的答案",traceback.print_exc())
