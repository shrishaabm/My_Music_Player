from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

import mysql.connector as m

bCOLOR = "#e84f54"

root=Tk()
root.geometry('600x450')
root.configure(background=bCOLOR)

pygame.mixer.init()

k=m.connect(host='localhost',user='root',passwd='tiger',database='music')
c = k.cursor()

#FUNCTIONS
def playtime():
    if stopped:
      return True
    curr=pygame.mixer.music.get_pos()/1000
    min_time=time.strftime('%M:%S',time.gmtime(curr))
    # bar.config(text=min_time)
    bar.after(1000,playtime)
    if cursong[0]: # playlist view OR default view
      song = songs[ songsl[cursong[1]] ]
    else:
      song = songs[ list(songs.keys())[cursong[1]] ]
      # songs.keys()
    mut=MP3(song)
    global song_len
    song_len=mut.info.length
    conv_time=time.strftime('%M:%S',time.gmtime(song_len))
    curr+=1
    if int(slider.get())==int(song_len):
        bar.config(text=f'{conv_time} ')
        return True

    elif paused:
        pass

    elif int(slider.get())==int(curr):
        if stopped:
            return True
        slider_pos=int(song_len)
        slider.config(to=slider_pos,value=int(curr))
    else:
        if stopped:
            return True

        slider_pos=int(song_len)
        slider.config(to=slider_pos,value=int(slider.get()))
        min_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))
        bar.config(text=f'{min_time} of {conv_time} ')
        next_time=int(slider.get())+1
        slider.config(value=int(next_time))

def play():
    global cursong

    if not pview:
      idx = 0
      if list_box.index(ACTIVE) >= 0:
        idx = list_box.index(ACTIVE)
      song=list_box.get(idx)
      song=f'songs/{song}'
      # bar.config(text=time.strftime('%M:%S',time.gmtime(MP3(song).info.length)))
    else:
      idx = 0
      if list_box_2.index(ACTIVE) >= 0:
        idx = list_box_2.index(ACTIVE)
      song = "songs/{}".format(list_box_2.get(idx))

    cursong = pview, idx

    stopped=False
    slider.config(value=0)
    bar.config(text='')
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    playtime()

stopped=False
def stop():

    bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()
    list_box.selection_clear(ACTIVE)
    list_box_2.selection_clear(ACTIVE)
    global stopped
    stopped=True
    playtime()

def next_song():
    global cursong
    cursong = pview, cursong[1] + 1

    if pview:
      if cursong[1] >= len(songsl):
        cursong[1] = len(songsl) - 1
    else:
      if cursong[1] >= len(songs):
        cursong[1] = len(songs) - 1

    if cursong[0]:
      try:
        song = songs[songsl[cursong[1]]]
      except IndexError:
        song = songs[songsl[0]]
        cursong = cursong[0], 0

    else:
      try:
        song = songs[list(songs.keys())[cursong[1]]]
      except IndexError:
        song = songs[list(songs.keys())[0]]
        cursong = cursong[0], 0

    bar.config(text='')
    slider.config(value=0)
    # next=list_box.curselection()
    # if pview:
    #   next = list_box_2.curselection()
    # if not len(next) == 0:
    #   next=next[0]+1
    # else:
    #   next = 0
    # print(next)
    try:
      pygame.mixer.music.load(song)
      pygame.mixer.music.play()
    except pygame.error:
      pygame.mixer.music.stop()
      pygame.mixer.music.rewind()


    list_box.selection_clear(0,END)
    list_box.activate(cursong[1])
    list_box.selection_set(cursong[1],last=None)
    playtime()

def previous_song():
    global cursong
    cursong = pview, cursong[1] - 1

    if cursong[1] == -1:
      cursong = cursong[0], 0
    if cursong[0]:
      try:
        song = songs[songsl[cursong[1]]]
      except IndexError:
        song = songs[songsl[0]]
        cursong = cursong[0], 0

    else:
      try:
        song = songs[list(songs.keys())[cursong[1]]]
      except IndexError:
        song = songs[list(songs.keys())[0]]
        cursong = cursong[0], 0

    bar.config(text='')
    slider.config(value=0)
    try:
      pygame.mixer.music.load(song)
      pygame.mixer.music.play()
    except pygame.error:
      pygame.mixer.music.stop()
      pygame.mixer.music.rewind()


    list_box.selection_clear(0,END)
    list_box.activate(cursong[1])
    list_box.selection_set(cursong[1],last=None)
    playtime()

paused=False

def pause():
    global paused, stopped
    stopped = True

    if paused==True:
        pygame.mixer.music.unpause()
        paused=False
        stopped = False
        playtime()
    else:
        pygame.mixer.music.pause()
        paused=True


def delete_song():
  if pview:
    song = list_box_2.get(ACTIVE)
    songsl.remove(song)
    list_box_2.delete(0, END)
    for n in songsl:
      list_box_2.insert(END, n)
  else:
    stop()
    list_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def deleteall_songs():
    stop()
    list_box.delete(0,END)
    pygame.mixer.music.stop()

def update_songs():
    global songs, songsl

    list_box.delete(0, END)
    # list_box_for_library.delete(0, END)

    for n in songs.items():
        # ((name, path), (name2, path2))
        # (name, path)
        # list.insert(0, "item")
        list_box.insert(END, n[0])

def slide(x):
    pygame.mixer.music.stop()
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(start=int(slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume=pygame.mixer.music.get_volume()
    volume_label.config(text=int(current_volume * 100))

def add_song():
    global songsl
    song = list_box.get(ACTIVE)
    songsl.append(song)

def toggleplaylist():
    global pview

    # list_box.delete(0, END)
    list_box.grid_forget()
    list_box_2.grid_forget()
    if not pview:
        pview = True
        add_songs_button.grid_forget()
        list_box_2.grid(row=0, column=0)
        list_box_2.delete(0, END)
        for n in songsl:
            list_box_2.insert(END, n)
    else:
        pview = False
        add_songs_button.grid(row=0,column=0,padx=10)
        list_box.grid(row=0, column=0)

#FRAMES FOR MAIN PLAYER:-
#MASTER FRAME
master_frame= Frame(root, background=bCOLOR)
master_frame.pack(pady=20)

#VOLUME FRAME
volume_frame=LabelFrame(master_frame,text='Volume')
volume_frame.grid(row=0,column=1,padx=20)

#LIST BOX
list_box=Listbox(master_frame,bg='black',fg='green',width=60,selectbackground='gray',selectforeground='black')
list_box.grid(row=0,column=0)

list_box_2 = Listbox(master_frame,bg='black',fg='green',width=60,selectbackground='gray',selectforeground='black')


pview = False
cursong = pview, None
songs = {}
songsl = []

#SONGS FROM MYSQL
# name, path, title, artist, album
c.execute("SELECT * FROM musiclist")
# [[n,p,t,a,a], [n,p,t,a,a]]
# [a, b]
for song in c.fetchall():
    # [n,p,t,a,a]
    songs[ song[0] ] = song[1]  # {name: path, ...}
update_songs()

#BUTTONS IMAGES
back_img=PhotoImage(file='./images(blue)/previou2.png')
forward_img=PhotoImage(file='./images(blue)/next2.png')
play_img=PhotoImage(file='./images(blue)/play2.png')
pause_img=PhotoImage(file='./images(blue)/pause2.png')
stop_img=PhotoImage(file='./images(blue)/stop2.png')
home_img=PhotoImage(file='./images(blue)/home.png')
playlist_img=PhotoImage(file='./images(blue)/pl.png')
add_songs_img=PhotoImage(file='./images(blue)/add songs.png')


frame=Frame(master_frame, background=bCOLOR)
frame.grid(row=1,column=0,pady=20)

#BUTTONS
back_button=Button(frame,image=back_img, background=bCOLOR,borderwidth=0,command=previous_song)
forward_button=Button(frame,image=forward_img, background=bCOLOR,borderwidth=0,command=next_song)
play_button=Button(frame,image=play_img, background=bCOLOR,borderwidth=0,command=play) # play button
pause_button=Button(frame,image=pause_img, background=bCOLOR,borderwidth=0,command=pause)
stop_button=Button(frame,image=stop_img, background=bCOLOR,borderwidth=0,command=stop) # stop image
playlist_button=Button(frame,image=playlist_img, background=bCOLOR,command=toggleplaylist)
add_songs_button=Button(frame,image=add_songs_img, background=bCOLOR,command=add_song)
# home_button=Button(library_frame,image=home_img, command=toggleplaylist)


#BUTTON PLACEMENT
back_button.grid(row=0,column=1,padx=10)
forward_button.grid(row=0,column=2,padx=10)
play_button.grid(row=0,column=3,padx=10)
pause_button.grid(row=0,column=4,padx=10)
stop_button.grid(row=0,column=5,padx=10)
#home_button.grid(row=0, column=1,pady=250)
playlist_button.grid(row=0,column=7,padx=10)
add_songs_button.grid(row=0,column=0,padx=10)

#MENU
my_menu=Menu(root)
root.config(menu=my_menu)

remove_song=Menu(my_menu)
my_menu.add_cascade(label='Remove song',menu=remove_song)
remove_song.add_command(label='Delete A song',command=delete_song)
remove_song.add_command(label='Delete All song',command=deleteall_songs)

bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
bar.pack(fill='x',side=BOTTOM,ipady=2)

slider=ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
slider.grid(row=2,column=0,pady=10)

volume_slider=ttk.Scale(volume_frame,from_=0,to=1,value=1,orient=VERTICAL,command=volume,length=130)
volume_slider.pack(pady=10)

volume_label=Label(volume_frame,text='')
volume_label.pack(pady=10)
root.mainloop()
