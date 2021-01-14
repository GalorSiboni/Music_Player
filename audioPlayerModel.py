from pygame import mixer
import time
##THIS MODEL CLASS IS THE Logic IMPLEMENTATION OF ALL THE BUTTON ON THE GUI

#model
class audioPlayerModel:
 def __init__(self, view):

  self.play=False
  self.paused=False
  self.stop=False
  self.play_list = []
  self.playListIterator = playList(self.play_list,view,self)
  self.view = view
  self.muted = False
  self.current_song = None
  mixer.init()


 def play_Music(self):
     self.stop=False
     if self.paused:
         #mixer.music.unpause()
         mixer.music.play(start=int(self.view.my_slider.get()))
         self.paused=False
         self.play=True
     else:
         try:
             if self.play is False:
                 time.sleep(1)
                 selected_song = self.view.list_song.curselection()
                 current_selected = int(selected_song[0])
                 self.current_song = self.play_list[current_selected]
                 mixer.music.load(self.current_song)
                 mixer.music.play(self.view.my_slider.get())
                 self.play = True
                 self.view.show_details(self.current_song)
         except:
          return None

 def del_song(self,selected_song):
     self.stop_Music()
     self.play_list.pop(selected_song)

 def add_to_playlist(self,filename):
  index = len(self.play_list)
  self.play_list.insert(index, filename)
  self.current_song = self.play_list[0]


 def mute_Music(self):
    if self.muted:
        mixer.music.set_volume(0.7)
        self.view.scale.set(70)
        self.muted = False
    else:
        mixer.music.set_volume(0)
        self.view.scale.set(0)
        self.muted = True


 def stop_Music(self):
     #self.pasued = False
     self.play = False
     self.stop=True
     mixer.music.stop()

 def set_volume(self,val):
    if self.muted is True:
        return
    volume =int(val)/100
    mixer.music.set_volume(volume)





 def pause_Music(self):
    self.paused=True
    self.play=False
    mixer.music.pause()

 def previous_Music(self):
  self.stop = True
  self.playListIterator.prev()
  self.view.my_slider.config(value=0)

 def next_Music(self):
     self.stop = True
     self.playListIterator.next()
     self.view.my_slider.config(value=0)

 def slider_Music(self):
     if self.paused==False:
        mixer.music.play(start=int(self.view.my_slider.get()))



 def write_List_To_File(self, lines):
     list = []
     list = lines
     while '\n' in list: list.remove('\n')
     with open("MP3MusicList.txt", "w", encoding='UTF-8') as playlist_File:
         if(len(list) == 0):
             playlist_File.close()
         else:
             playlist_File.write('\n'.join(list))
             playlist_File.close()

class playList:
    def __init__(self, list,view,model):
        self.list = list
        self.index = 0
        self.current_song=None
        self.view=view
        self.model=model

    def next(self):
        try:
            time.sleep(1)
            self.view.model.stop=False
            result = self.list[self.index]
            self.index += 1
            self.current_song = self.list[self.index]
            mixer.music.load(self.current_song)
            mixer.music.play()
            self.view.show_details(self.current_song)

        except IndexError:
            self.index = 0
            result = self.list[self.index]
            self.current_song = self.list[self.index]
            mixer.music.load(self.current_song)
            mixer.music.play()
            self.view.show_details(self.current_song)
        return result

    def prev(self):
        time.sleep(1)
        self.view.model.stop = False
        self.index -= 1
        if self.index < 0:
            self.index = len(self.list)-1
            self.current_song = self.list[self.index]
            mixer.music.load(self.current_song)
            mixer.music.play()
            self.view.show_details(self.current_song)
        else:
            self.current_song = self.list[self.index]
            mixer.music.load(self.current_song)
            mixer.music.play()
            self.view.show_details(self.current_song)
            return self.list[self.index]

    def __iter__(self):
        return self




