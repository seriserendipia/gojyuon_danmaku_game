import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class Team:

    def __init__(self,team_flag:str):
        self.team_flag = team_flag
        self.member_list = []
        self.score = 0

    def add_member(self,nickname):
        self.member_list.append(nickname)

    def is_nickname_in_this_team(self,nickname):
        if nickname in self.member_list:
            return True
        return False

    def add_score(self,score):
        self.score += score

    def get_score(self):
        return self.score



class TeamInfo(QThread):
    new_player_message_Signal = QtCore.pyqtSignal(str)
    refresh_team_list_Signal = QtCore.pyqtSignal(str,str)

    def __init__(self):
        super(TeamInfo, self).__init__()
        self.team_list = []
        self.team_red = Team("红")
        self.team_blue = Team("蓝")
        self.team_list.append(self.team_red)
        self.team_list.append(self.team_blue)


    def get_team_flag(self,nickname):
        for i in self.team_list:
            if i.is_nickname_in_this_team(nickname):
                return i.team_flag

        raise Exception(f"该昵称{nickname}尚未分配队伍")

    def get_player_assign_team(self, nickname):
        try:
            return self.get_team_flag(nickname)
        except Exception as e:
            print(str(e))
            if len(self.team_red.member_list) > len(self.team_blue.member_list):
                team = self.team_blue
            else:
                team = self.team_red
            team.add_member(nickname)
            new_player_message = f"{nickname}开始游戏，加入{team.team_flag}队"
            self.new_player_message_Signal.emit(new_player_message)
            self.refresh_team_list_Signal.emit(team.team_flag,nickname)
            return team.team_flag

    def get_team_from_flag(self,team_flag):
        for i in self.team_list:
            if team_flag == i.team_flag:
                return i
        raise Exception(f"输入的队伍名{team_flag}不在现有的队伍列表之中")

    def add_score(self,score, team_flag):
        team = self.get_team_from_flag(team_flag)
        team.add_score(score)
