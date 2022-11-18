import numpy as np
import pandas as pd

#%%
TEST_ROOM_IDS = [
    26431522
]

# %%
blank_label_fill_str = """
        """

# %%
hiraganastr = """あいうえお
かきくけこ
さしすせそ
たちつてと
なにぬねの
はひふへほ
まみむめも
や　ゆ　よ
らりるれろ
わ　　　を
ん　　　　
""".encode("utf-8").decode("utf-8")

kataganastr = """アイウエオ
カキクケコ
サシスセソ
タチツテト
ナニヌネノ
ハヒフヘホ
マミムメモ
ヤ　ユ　ヨ
ラリルレロ
ワ　　　ヲ
ン　　　　
""".encode("utf-8").decode("utf-8")

roumaji = np.array([["a", "i", "u", "e", "o", ],
                    ["ka", "ki", "ku", "ke", "ko", ],
                    ["sa", "shi", "su", "se", "so", ],
                    ["ta", "chi", "tsu", "te", "to", ],
                    ["na", "ni", "nu", "ne", "no", ],
                    ["ha", "hi", "fu", "he", "ho", ],
                    ["ma", "mi", "mu", "me", "mo", ],
                    ["ya", " ", "yu", " ", "yo", ],
                    ["ra", "ri", "ru", "re", "ro", ],
                    ["wa", " ", " ", " ", "wo", ],
                    ["n", " ", " ", " ", " ", ]])

# %%
# def gen_array(str1):
#     print("[[",end="",sep = "")
#     for i in str1:
#         if i == "\n":
#             print("],\n[",end="",sep = "")
#         else:
#             print("'",i,end="',",sep="")
#     print("]",end="",sep = "")
#     print()
#
# gen_array(hiraganastr)
# gen_array(kataganastr)
# %%
hiragana_df = pd.DataFrame([['あ', 'い', 'う', 'え', 'お', ],
                            ['か', 'き', 'く', 'け', 'こ', ],
                            ['さ', 'し', 'す', 'せ', 'そ', ],
                            ['た', 'ち', 'つ', 'て', 'と', ],
                            ['な', 'に', 'ぬ', 'ね', 'の', ],
                            ['は', 'ひ', 'ふ', 'へ', 'ほ', ],
                            ['ま', 'み', 'む', 'め', 'も', ],
                            ['や', '　', 'ゆ', '　', 'よ', ],
                            ['ら', 'り', 'る', 'れ', 'ろ', ],
                            ['わ', '　', '　', '　', 'を', ],
                            ['ん', '　', '　', '　', '　', ]])

katagana_df = pd.DataFrame([['ア', 'イ', 'ウ', 'エ', 'オ', ],
                            ['カ', 'キ', 'ク', 'ケ', 'コ', ],
                            ['サ', 'シ', 'ス', 'セ', 'ソ', ],
                            ['タ', 'チ', 'ツ', 'テ', 'ト', ],
                            ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ', ],
                            ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ', ],
                            ['マ', 'ミ', 'ム', 'メ', 'モ', ],
                            ['ヤ', '　', 'ユ', '　', 'ヨ', ],
                            ['ラ', 'リ', 'ル', 'レ', 'ロ', ],
                            ['ワ', '　', '　', '　', 'ヲ', ],
                            ['ン', '　', '　', '　', '　', ]])
# %%
hiragana = hiragana_df.to_numpy()
hiragana
katakana = katagana_df.to_numpy()
katakana

#%%
kanasets = [hiragana, katakana, roumaji]

# %%

def shuffle(kana_range: np.array):
    random_kana = np.random.choice(kana_range.flatten(), 1)[0]
    while random_kana == '\u3000':
        random_kana = np.random.choice(kana_range.flatten(), 1)[0]
    return random_kana


shuffle(hiragana)
# %%


# %%
def parseChar_key_from_to(keychar,from_charset,to_charset):
    key_index = np.argwhere(from_charset == keychar)
    return to_charset[key_index[0, 0], key_index[0, 1]]

# %%
def get_hiragana(q_roumaji):
    return parseChar_key_from_to(q_roumaji,roumaji,hiragana)


def get_katakana(q_roumaji):
    return parseChar_key_from_to(q_roumaji,roumaji,katakana)


def get_roumaji_from_hirakana(kana):
    return parseChar_key_from_to(kana,hiragana,roumaji)


def get_roumaji_from_katakana(kana):
    return parseChar_key_from_to(kana,katakana,roumaji)


def get_roumaji(kana):
    if kana in hiragana:
        return get_roumaji_from_hirakana(kana)
    elif kana in katakana:
        return get_roumaji_from_katakana(kana)
    else:
        return kana
