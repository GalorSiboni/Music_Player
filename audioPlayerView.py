from tkinter import *
import tkinter.messagebox
import os
from tkinter import filedialog
from audioPlayerModel import audioPlayerModel
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
import tkinter.ttk as ttk


## THIS CLASS IS ONLY TAKE CARE OF THE GUI PART OF THIS APP
class audioPlayerView:
    def __init__(self):
        #init Tkitner
        self.total_length=0
        self.current_time=0
        self.lines = []
        self.root = Tk()
        self.root.title("Afeka tunes")
        self.root.iconbitmap(r'play_button_JpT_icon.ico')

        menubar = Menu(self.root)  # create menubar
        self.root.config(menu=menubar)



        # create status massage
        statusbar = Label(self.root, text="Welcom to my player", relief=SUNKEN)
        statusbar.pack(side=BOTTOM, fill=X)
        self.statusbar=statusbar





        submenu = Menu(menubar)

        #left frame
        left_frame = Frame(self.root)
        left_frame.pack(side=LEFT, padx=30)

        #right frame
        right_frame = Frame(self.root)
        right_frame.pack(side=RIGHT)

        #middle frame
        middle_frame = Frame(right_frame)
        middle_frame.pack(padx=10, pady=10)


        top_frame = Frame(right_frame)
        top_frame.pack()

        middle_frame = Frame(right_frame)
        middle_frame.pack(padx=10, pady=10)

        #buttom frame
        bottomframe = Frame(right_frame)
        bottomframe.pack()


        self.lenght_lable = Label(top_frame, text="Totel length :00:00 ")
        self.lenght_lable.pack()

        self.curren_Time_lable = Label(top_frame, text="current Time  :00:00 ")
        self.curren_Time_lable.pack()  #

        list_song = Listbox(left_frame)
        list_song.pack()
        self.list_song = list_song
        self.model = audioPlayerModel(self)
        self.load_Playlist_From_File()

        #images
        self.play_photo = PhotoImage(file='play-button.png')
        self.volume_photo = PhotoImage(file='volume.png')
        self.mute_photo = PhotoImage(file='mute.png')
        self.stop_photo = PhotoImage(file='stop.png')
        self.pause_photo = PhotoImage(file='pause.png')
        self.next_photo = PhotoImage(file='next.png')
        self.previous_photo = PhotoImage(file='previous.png')


        self.add_btn = Button(left_frame, text="Add",command=self.browse_file)
        self.add_btn.pack(side=LEFT, padx=10)


        self.del_btn = Button(left_frame, text="Delete",command=self.update_Delet_Song)
        self.del_btn.pack(side=LEFT)


        self.btn_mute = Button(bottomframe, image=self.volume_photo, command=self.update_Mute_Music)
        self.btn_mute.grid(row=0, column=1)

        self.btn_play = Button(middle_frame, image=self.play_photo,command=self.update_Play_Music)
        self.btn_play.grid(row=0, column=1, padx=10)

        self.btn_stop = Button(middle_frame, image=self.stop_photo, command=self.update_Stop_Music)
        self.btn_stop.grid(row=0, column=2, padx=10)

        self.btn_pause = Button(middle_frame, image=self.mute_photo, command=self.update_Pause_Music)

        self.btn_next = Button(middle_frame, image=self.next_photo, command=self.update_Next_Music)
        self.btn_next.grid(row=0, column=3)

        self.btn_previous = Button(middle_frame, image=self.previous_photo, command=self.update_Previous_Music)
        self.btn_previous.grid(row=0, column=0, )

        self.scale = Scale(bottomframe, from_=0, to=100, orien=HORIZONTAL,command=self.model.set_volume)  # scale of the valum
        self.scale.set(50)  # set the initial valume to be 50
        mixer.music.set_volume(0.5)
        self.scale.grid(row=0, column=2, pady=15, padx=30)

        #create slider of the song time
        self.my_slider=ttk.Scale(top_frame, from_=0, to_=100, orient=HORIZONTAL, value=0,
        command=self.slide_Music, length=250)
        self.my_slider.pack(side=BOTTOM)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    #this function open the browse file to choose one file
    def browse_file(self):
        global filePath
        filePath = filedialog.askopenfilename()
        if(filePath != ''):
          filename = os.path.basename(filePath)
          index = self.list_song.size()
          self.list_song.insert(index, filename)
          self.list_song.pack()
          self.model.add_to_playlist(filePath)
          self.lines.insert(index, filePath)
          lastIndex = len(self.lines)
          if lastIndex > 0:
            self.list_song.selection_clear(0)
            self.list_song.activate(0)
            self.list_song.selection_set(0)




    def load_Playlist_From_File(self):
        try:
            with open("MP3MusicList.txt", "r", encoding='UTF-8') as playlist_File:
                list = playlist_File.readlines()
                for element in list:
                    if not element.isspace():
                        self.lines.append(element)
                for filePath in self.lines:
                    index = self.list_song.size()
                    f = os.path.basename(filePath.rstrip())
                    self.list_song.insert(index, f)
                    self.list_song.pack()
                    self.model.add_to_playlist(filePath.rstrip())  # need to check if there is another wey to make butter implemantation
                    lastIndex = len(self.lines)
                    if lastIndex > 0:
                        self.list_song.selection_clear(0)
                        self.list_song.activate(0)
                        self.list_song.selection_set(0)

        except:
            print("file not found")
            playlist_File = open("MP3MusicList.txt", "w+", encoding='UTF-8')


    def update_Play_Music(self):
        if(self.model.play):
            self.update_Pause_Music()
            return

        self.model.play_Music()
        if(self.model.current_song!=None):
            self.statusbar['text'] = "playing music  " + os.path.basename(self.model.current_song)
        else:
            tkinter.messagebox.showerror("Eror", "Not found music to play !")
        if(self.model.play):
            self.btn_play.configure(image=self.pause_photo)


    def update_Delet_Song(self):
        selected_song = self.list_song.curselection()
        self.list_song.delete(selected_song)
        selected_song = int(selected_song[0])
        self.lines.pop(selected_song) #delete the selected song
        self.model.del_song(selected_song)
        if (selected_song > 0):
            self.list_song.activate(selected_song - 1)
            self.list_song.selection_set(selected_song - 1)
        if (selected_song == 0 and len(self.lines) != 0):
            self.list_song.activate(selected_song)
            self.list_song.selection_set(selected_song)
        self.btn_play.configure(image=self.play_photo)
        self.my_slider.config(value=0)
        self.show_current_time(0)
        self.show_total_time(0)

    def update_Mute_Music(self):
      self.model.mute_Music()
      if(self.model.muted):
       self.btn_mute.configure(image=self.mute_photo)
      else:
       self.btn_mute.configure(image=self.volume_photo)

    def update_Stop_Music(self):
        self.model.stop_Music()
        self.statusbar['text'] = "Music Stop"
        self.btn_play.configure(image=self.play_photo)
        self.my_slider.config(value=0)
        self.show_current_time(0)


   #show current time of song and show on the screen
    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)
        if file_data[1] == ".mp3":
            audio = MP3(play_song)
            self.total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            self.total_length = a.get_length()

        self.show_total_time(self.total_length)
        self.statusbar['text'] = "playing music  " + os.path.basename(play_song)
        t1 = threading.Thread(target=self.start_count, args=(self.total_length,))
        t1.start()


    #start to count the time in different thread.
    def start_count(self,total_length):
      # mixer.music.get.busy=return fal se when we press stop music
      self.current_time=0
      while self.current_time<=total_length and mixer.music.get_busy():
         if self.model.paused:
             continue

         if self.model.stop:
             return

         else:
          self.show_current_time(self.current_time)
          if(self.my_slider.get()==int(self.total_length)):
              pass

          if(self.model.paused):
              pass

          elif(self.my_slider.get()==int(self.current_time)):
            slider_position=int(self.total_length)
            self.my_slider.config(to=slider_position,value=int(self.current_time))
          else:
              slider_position = int(self.total_length)
              self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
              next_time=int(self.my_slider.get()+1)
              self.show_current_time(next_time)
              self.my_slider.config(value=next_time)

          time.sleep(1)
          self.current_time+=1


    def update_Pause_Music(self):

        self.model.pause_Music()
        self.btn_play.configure(image=self.play_photo)
        self.statusbar['text'] = "Music pause"

    def update_Next_Music(self):
        if self.model.current_song != None and len(self.lines) > 0:
            self.model.next_Music()
            self.next_selection()

        else:
            tkinter.messagebox.showerror("Eror", "The List is Empty!")

    def update_Previous_Music(self):
        if self.model.current_song != None and len(self.lines) > 0:
            self.model.previous_Music()
            self.perv_selection()
        else:
            tkinter.messagebox.showerror("Eror", "The List is Empty!")



    def slide_Music(self,x):
        self.model.slider_Music()

    def show_current_time(self,time):
        mint, sec = divmod(time, 60)
        mint = round(mint)
        sec = round(sec)
        time_formet = '{:02d}:{:02d}'.format(mint, sec)  # make the format text
        self.curren_Time_lable['text'] = "Current time  " + ' - ' + time_formet  # show total length of song


    ##show totel legnth of song
    def show_total_time(self,time):
        mint, sec = divmod(time, 60)
        mint = round(mint)
        sec = round(sec)
        time_formet = '{:02d}:{:02d}'.format(mint, sec)  # make the format text
        self.lenght_lable['text'] = "Total length  " + ' - ' + time_formet  # show total length of song time

    def next_selection(self):
        selection_indices = self.list_song.curselection()

        # default next selection is the beginning
        next_selection = 0

        # make sure at least one item is selected
        if len(selection_indices) > 0:
            # Get the last selection, remember they are strings for some reason
            # so convert to int
            last_selection = int(selection_indices[-1])
            next_selection = last_selection + 1
        if int(selection_indices[-1]) == self.list_song.size() - 1:
            last_selection = int(selection_indices[-1])
            next_selection = 0

        self.list_song.selection_clear(last_selection)
        self.list_song.activate(next_selection)
        self.list_song.selection_set(next_selection)

    def perv_selection(self):
        selection_indices = self.list_song.curselection()

        # default next selection is the beginning
        next_selection = 0

        # make sure at least one item is selected
        if len(selection_indices) == self.list_song.size() - 1:
            # Get the last selection, remember they are strings for some reason
            # so convert to int
            last_selection = int(selection_indices[-1])
            next_selection = last_selection - 1
        if int(selection_indices[-1]) == 0:
            last_selection = 0
            next_selection = self.list_song.size() - 1

        self.list_song.selection_clear(last_selection)
        self.list_song.activate(next_selection)
        self.list_song.selection_set(next_selection)


    def update_set_Volume(self):
       self.btn_mute.configure(image=self.volume_photo)

   # function that start when we press to exit from the audioPlayer response to write the current songs to the file.
    def on_closing(self):
        self.model.stop_Music()
        self.model.write_List_To_File(self.lines)
        self.root.destroy()