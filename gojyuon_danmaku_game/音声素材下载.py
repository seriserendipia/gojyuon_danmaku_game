# %%
import os
import sys

currentPath = r"D:\PythonEx\casualProject\五十音互动"
print(currentPath)
sys.path.append(currentPath)

from 五十音互动.gojyuon_danmaku_game.initdata import *


# %%
def char_set_iter(kana_or_roumaji_sets: np.ndarray, func):
    l1 = []
    for i in np.nditer(kana_or_roumaji_sets):
        i = str(i)
        if i.strip() != "":
            l1.append(func(i))
    return l1


roumaji_chars = char_set_iter(roumaji, lambda i: i)
# %%
roumaji_chars
# %%
import requests

for roumaji_char in roumaji_chars:
    url = "https://www.coscom.co.jp/hiragana-katakana/au50on/kana50on_%s.mp3" % roumaji_char
    print("打开链接", url)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    audio_file = requests.get(url, headers=headers, timeout=3)
    print(audio_file)
    save_file_name = url.split("/")[-1]
    with open(os.path.join(r"/五十音互动/音声素材", save_file_name), "wb+") as f:
        f.write(audio_file.content)
        print("下载", save_file_name, "成功")
