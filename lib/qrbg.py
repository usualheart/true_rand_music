import time
from threading import Thread

import requests
from cffi.cparser import lock


class qrbg():
    def __init__(self,thread_num=1,random_pool_size =1024):
        self.rbuf = []
        self.stop = False # 控制是否自动更新随机数池子的线程
        self.thread_num = thread_num
        self.random_pool_size = random_pool_size
        self.startUpdateThread()

    def startUpdateThread(self):
        for i in range(self.thread_num):
            t = Thread(target=self.updateRbuf)
            t.start()

    def updateRbuf(self):
        while (not self.stop and len(self.rbuf) < self.random_pool_size):
            res = requests.get('http://qrng.anu.edu.au/API/jsonI.php?length=100&type=uint16&size=1024')
            print('更新随机数池成功!')
            res = res.json()
            #print(res['data'])

            lock.acquire()
            self.rbuf.extend(res['data'])
            lock.release()

    def get_r_uint16(self):
        while len(self.rbuf) < 1:
            if self.stop:
                self.stop = False
                self.startUpdateThread()
            time.sleep(0.1)
        r_uint16 = self.rbuf.pop(0)  # 从表头取一个元素返回
        return r_uint16

    '''生成[0,n)的随机数
        参考python源代码中从0-1分布获取整数随机数的方法 https://github.com/python/cpython/blob/main/Lib/random.py
    '''

    def getRandomN(self, n):
        maxsize = 65536
        rem = maxsize % 40
        limit = (maxsize - rem)  # limit  % n == 0
        r_uint16 = self.get_r_uint16()
        while r_uint16 >= limit:
            r_uint16 = self.get_r_uint16()
        return r_uint16 % n
        uint16

    """生成[m,n)的随机数"""

    def getRandomInt(self, m, n):
        return m + self.getRandomN(n - m)


if __name__ == '__main__':
    # 测试
    qrbg = qrbg()

    cnt = [0, 0, 0, 0, 0]
    for i in range(1000):
        # print(qrbg.get_r_uint16())
        # tmp = qrbg.getRandomN(5)
        tmp = qrbg.getRandomInt(1, 6)
        cnt[tmp - 1] += 1
        print(tmp)
    print(cnt)
    # qrbg.stop = True
    # qrbg.getRandomInt(1, 6)
