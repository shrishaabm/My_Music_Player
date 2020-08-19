from tkinter import*
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
        return
    curr=pygame.mixer.music.get_pos()/1000
    min_time=time.strftime('%M:%S',time.gmtime(curr))
    # bar.config(text=min_time)
    bar.after(1000,playtime)
    curr_song=list_box.curselection()
    song=list_box.get(ACTIVE)
    song=f'songs/{song}'
    mut=MP3(song)
    global song_len
    song_len=mut.info.length
    conv_time=time.strftime('%M:%S',time.gmtime(song_len))
    curr+=1
    if int(slider.get())==int(song_len):
        bar.config(text=f'{conv_time} ')

    elif paused:
        pass

    elif int(slider.get())==int(curr):
        slider_pos=int(song_len)
        slider.config(to=slider_pos,value=int(curr))
    else:

        slider_pos=int(song_len)
        slider.config(to=slider_pos,value=int(slider.get()))
        min_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))
        bar.config(text=f'{min_time} of {conv_time} ')
        next_time=int(slider.get())+1
        slider.config(value=int(next_time))


def play():
    stopped=False
    slider.config(value=0)
    song=list_box.get(ACTIVE)
    song=f'songs/{song}'
    bar.config(text='')
    # bar.config(text=time.strftime('%M:%S',time.gmtime(MP3(song).info.length)))
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    playtime()


global stopped
stopped=False
def stop():
    bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()
    global stopped
    stopped=True

def next_song():
    bar.config(text='')
    playtime()
    # bar.config(text=time.strftime('%M:%S',time.gmtime(MP3(song).info.length)))
    slider.config(value=0)
    next=list_box.curselection()
    next=next[0]+1
    print(next)
    song=list_box.get(next)
    song=f'songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    list_box.selection_clear(0,END)
    list_box.activate(next)
    list_box.selection_set(next,last=None)

def previous_song():
    bar.config(text='')
    playtime()
    # bar.config(text=time.strftime('%M:%S',time.gmtime(MP3(song).info.length)))
    slider.config(value=0)
    previous=list_box.curselection()
    previous=previous[0]-1
    print(previous)
    song=list_box.get(previous)
    song=f'songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    list_box.selection_clear(0,END)
    list_box.activate(previous)
    list_box.selection_set(previous,last=None)

paused=False

def pause():
    global paused
    # paused=is_paused

    if paused==True:
        pygame.mixer.music.unpause()
        paused=False
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
        list_box.insert(END, n[0])

    # for n in songsl:
        # list_box_for_library.insert(END, n)

def slide(x):
    pygame.mixer.music.set_pos(int(slider.get()))


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
        # for n in songs:
        #     list_box.insert(END, n)

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
songs = {}
songsl = []

#SONGS FROM MYSQL
c.execute("SELECT * FROM musiclist")
for song in c.fetchall():
    songs[song[0]] = song[1]
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
