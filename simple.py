# 只可播放单首 无法连续播放
import os
from lib.qrbg import qrbg
music_folder = ["D:\\Users\\yu\\Music\\flac\\","D:\\Users\\yu\\Music\\mp3\\"]
music_list = []
for path in music_folder:
    for file in os.listdir(path):
        music_list.append(path+file)
# 真随机数生成器
qrbg =qrbg(random_pool_size=100)
mingling = 'n'
while(1):
    mingling = input("请输入命令，下一曲n：")
    print(mingling)
    print()
    if mingling==''  or mingling[0] in ['n','N','\n']: # 如果输入回车或者n 下一曲
        music = music_list[qrbg.getRandomN(len(music_list))]
        os.system("\""+music+"\"")