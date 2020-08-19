from tkinter import*
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()
root.geometry('600x450')

pygame.mixer.init()

#FUNCTIONS
def playtime():
    if stopped:
        return
    curr=pygame.mixer.music.get_pos()/1000
    #slider_label.config(text=f'Slider:{int(slider.get())}')
    min_time=time.strftime('%M:%S',time.gmtime(curr))
    bar.config(text=min_time)
    bar.after(1000,playtime)
    curr_song=list_box.curselection()
    song=list_box.get(ACTIVE)
    song=f'D:/shrishaa/python project/songs/{song}'
    mut=MP3(song)
    global song_len
    song_len=mut.info.length
    conv_time=time.strftime('%M:%S',time.gmtime(song_len))
    #bar.config(text=f'{min_time} of {conv_time} ')
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
    

def addsong():
    song=filedialog.askopenfilename(initialdir='songs/',title='choose a song',filetype=(('mp3 Files','*mp3'),))
    print(song)
    song=song.replace('D:/shrishaa/python project/songs/','')
    list_box.insert(END,song)
    
    
    
def add_manysong():
    songs=filedialog.askopenfilenames(initialdir='songs/',title='choose a song',filetype=(('mp3 Files','*mp3'),))
    for song in songs:
        song=song.replace('D:/shrishaa/python project/songs/','')
        list_box.insert(END,song)
        
        
def play():
    stopped=False
    song=list_box.get(ACTIVE)
    song=f'D:/shrishaa/python project/songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    playtime()
    '''slider_pos=int(song_len)
    slider.config(to=slider_pos,value=0)'''
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
    slider.config(value=0)
    next=list_box.curselection()
    next=next[0]+1
    print(next)
    song=list_box.get(next)
    song=f'D:/shrishaa/python project/songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    list_box.selection_clear(0,END)
    list_box.activate(next)
    list_box.selection_set(next,last=None)
    musix.music.title
    
def previous_song():
    bar.config(text='')
    slider.config(value=0)
    previous=list_box.curselection()
    previous=previous[0]-1
    print(previous)
    song=list_box.get(previous)
    song=f'D:/shrishaa/python project/songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    list_box.selection_clear(0,END)
    list_box.activate(previous)
    list_box.selection_set(previous,last=None)

    
global paused
paused=False
    
def pause(is_paused):
    global paused
    paused=is_paused
    
    if paused==True:
        
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True
        

def delete_song():
    stop()
    list_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def deleteall_songs():
    stop()
    list_box.delete(0,END)
    pygame.mixer.music.stop()
    
    
def slide(x):
    song=list_box.get(ACTIVE)
    song=f'D:/shrishaa/python project/songs/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume=pygame.mixer.music.get_volume()
    volume_label.config(text=current_volume)
        
#MASTER FRAME
master_frame= Frame(root)
master_frame.pack(pady=20)

#VOLUME FRAME
volume_frame=LabelFrame(master_frame,text='Volume')
volume_frame.grid(row=0,column=1,padx=20)


#LIST BOX    
list_box=Listbox(master_frame,bg='black',fg='green',width=70,selectbackground='gray',selectforeground='black')
list_box.grid(row=0,column=0)

#BUTTONS IMAGES
back_img=PhotoImage(file='images(blue)/previou2.png')
forward_img=PhotoImage(file='images(blue)/next2.png')
play_img=PhotoImage(file='images(blue)/play2.png')
pause_img=PhotoImage(file='images(blue)/pause2.png')
stop_img=PhotoImage(file='images(blue)/stop2.png')

frame=Frame(master_frame)
frame.grid(row=1,column=0,pady=20)

#BUTTONS
back_button=Button(frame,image=back_img,borderwidth=0,command=previous_song)
forward_button=Button(frame,image=forward_img,borderwidth=0,command=next_song)
play_button=Button(frame,image=play_img,borderwidth=0,command=play)
pause_button=Button(frame,image=pause_img,borderwidth=0,command=lambda:pause(paused))
stop_button=Button(frame,image=stop_img,borderwidth=0,command=stop)

#BUTTON PLACEMENT
back_button.grid(row=0,column=0,pady=10)
forward_button.grid(row=0,column=1,pady=10)
play_button.grid(row=0,column=2,pady=10)
pause_button.grid(row=0,column=4,pady=10)
stop_button.grid(row=0,column=5,pady=10)

#MENU
my_menu=Menu(root)
root.config(menu=my_menu)

add_song=Menu(my_menu)
my_menu.add_cascade(label="add songs",menu=add_song)
add_song.add_command(label="Add one song",command=addsong)

add_song.add_command(label="Add more than one song",command=add_manysong)


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