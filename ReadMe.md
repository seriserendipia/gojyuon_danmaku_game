# 弹幕互动游戏：日语五十音记忆训练

通过网课学日语五十音，记忆效果有限。提问抢答需要老师手动播放音频、记分，会减慢课堂效率。尝试用b站直播弹幕互动游戏的形式，让课堂里的同学们都参与进来

- b站弹幕获取使用了 blivedm   
- GUI 用 PyQt5 写的  
- 五十音的音频来自 https://www.coscom.co.jp/hiragana-katakana/au50on/

### Game Rules
1. 游戏进行中发送任意内容弹幕，会随机被分到红组/蓝组，开始对战
2. 听写题：随机播放一个假名的发音 & 假名题：随机展示一个假名文字 
3. 观众可以发送该发音/假名对应的平假名、片假名、罗马音的弹幕答题
4. 答题判定取这条弹幕开头的内容
    >示例：【播放音频：あ】  
    正确回答：【a，A，あ，ア，a吧，ああああああ】  
    错误回答：【选あ，い，b，￥%^$，111，……】

5. 回答正确本组自动获得积分，抢到首杀和日语输入有额外加分可能
6. 只抓取弹幕，不支持其他特效，别碰打赏哦


### Usage
在data中设置本地路径、b站直播间ID、游戏的参数

### TODO
- 现在只有清音的数据，可以考虑加入浊音、半浊音、拗音
- 游戏参数设置界面GUI化
- 打包成.exe文件
- 得分数据想要持久化
- 个人重复得分（？
- 队伍列表显示个人得分，二连、三连、五连等特殊标识，连击加分

### 一些细节
每次暂停其实只是暂停了弹幕读取和出题限时，音频是每次都重新从头开始播放的
