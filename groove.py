import asyncio
import os
import time


from winrt.windows import system
from winrt.windows.media import MediaPlaybackAutoRepeatMode
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager,GlobalSystemMediaTransportControlsSessionPlaybackStatus
from winrt.windows.storage import StorageFile
import winrt.windows.media.control as wmc

config = open('config.txt','r')
music_folder = config.readlines()
config.close()
music_list = []
for path in music_folder:
    path = path.strip()
    for file in os.listdir(path):
        music_list.append(path+file)

class GrooveMusicCommand:
    def __init__(self):
        self._session = None

    @classmethod
    async def initializeSession(cls):
        """Get any session for Groove Music"""
        sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        currentSession = sessions.get_current_session()
        if currentSession and currentSession.source_app_user_model_id == "Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic":
            return currentSession
        return None

    async def getCurrentSession(self):
        """Return existing session or get a new session in case no existing session present"""
        if self._session is None:
            self._session = await self.initializeSession()

        return self._session

    @classmethod
    async def openMedia(cls, pathToAudioFile: str):
        """Open the file in Groove Music"""
        file = await StorageFile.get_file_from_path_async(os.fspath(pathToAudioFile))
        launcherOption = system.LauncherOptions()
        launcherOption.target_application_package_family_name = "Microsoft.ZuneMusic_8wekyb3d8bbwe"
        await system.Launcher.launch_file_async(file, launcherOption)

    async def play(self):
        """Play existing session"""
        session = await self.getCurrentSession()
        if session:
            session.try_play_async()

    async def pause(self):
        """Pause existing session"""
        session = await self.getCurrentSession()
        if session:
            session.try_pause_async()

        '''
    Changing	2	The media is changing.

    Closed	0	The media is closed.

    Opened	1	The media is opened.

    Paused	5	The media is paused.

    Playing	4	The media is playing.

    Stopped	3	The media is stopped.
    '''
    async def getMediaStates(self):
        session = await self.getCurrentSession()
        if session:
            return session.get_playback_info().playback_status
         
    async def changeRepeatMode(self, mode: str):
        """Change repeat mode of current session"""
        session = await self.getCurrentSession()
        if session:
            if mode == "current":
                session.try_change_auto_repeat_mode_async(MediaPlaybackAutoRepeatMode.TRACK)
            elif mode == "none":
                session.try_change_auto_repeat_mode_async(MediaPlaybackAutoRepeatMode.NONE)
            elif mode == "all":
                session.try_change_auto_repeat_mode_async(MediaPlaybackAutoRepeatMode.LIST)

        #get media state enum and compare to current main media session state   
        #return int(GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status 

    async def randomPlay(self):
        from lib.qrbg import qrbg
        qrbg =qrbg(random_pool_size=100)# 真随机数生成器
        music = music_list[qrbg.getRandomN(len(music_list))]
        await self.openMedia(music)
        time.sleep(3)
        while(1):
            mediaState = await self.getMediaStates()
            # print(mediaState)
            while mediaState==4:
                time.sleep(1)
                mediaState =  await self.getMediaStates()
                # print(mediaState)
            music = music_list[qrbg.getRandomN(len(music_list))]
            await self.openMedia(music)
            time.sleep(3)
            
            # mingling = input("下一曲按回车") # 无法区分播放完暂停还是手动暂停
            #if mediaState == 3 or mingling==''  or mingling[0] in ['n','N','\n']: # 如果音乐停止播放 输入回车或者n 下一曲
             

async def main():
    grooveMusicCommandObj = GrooveMusicCommand()
    await grooveMusicCommandObj.randomPlay()
    #await grooveMusicCommandObj.openMedia("D:\\Users\\yu\\Music\\flac\\Alan Walker - Alone [mqms2].flac")
    #await grooveMusicCommandObj.getMediaStates()
    #await grooveMusicCommandObj.changeRepeatMode("current")  # this works
    #time.sleep(5)
    #await grooveMusicCommandObj.pause()  # this also works fine
    #time.sleep(5)
    #time.sleep(5)
    #await grooveMusicCommandObj.play()  # this one works too
    #time.sleep(5)



if __name__ == "__main__":
    asyncio.run(main())