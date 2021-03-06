# true_rand_music

真随机音乐播放器！使用量子随机源产生的随机数来控制播放win10电脑里的音乐。

**真随机数来源**

>https://qrng.anu.edu.au/
>
>该网站向互联网上的任何人提供真正的随机数。我们实验室通过测量真空的量子涨落实时生成随机数。真空在量子物理学和经典物理学中的描述非常不同。在经典物理学中，真空被认为是没有物质或光子的空间。然而，量子物理学说，同一个空间就像一片虚拟粒子的海洋，一直在出现和消失。这是因为真空仍然具有零点能量。因此，真空的电磁场在所有频率上都表现出相位和幅度的随机波动。通过仔细测量这些波动，我们能够生成超高带宽的随机数。

**使用方法**

环境要求：python>3.7 win10 >=1809

- 安装依赖

  ```python
  pip install -r requirements.txt
  ```

- 编辑config.txt 每行一个填入音乐文件夹

- 双击 random_music.bat 即可。程序会从设置好的文件夹随机选一首歌曲播放。

**tips**

歌曲播放完会自动下一曲。

歌曲播放过程中点暂停，可以触发程序播放下一首随机歌曲。

**效果如下：**

![image-20220125231953639](img/image-20220125231953639.png)

