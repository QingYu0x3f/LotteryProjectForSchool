import random
from tkinter import messagebox
import tkinter
import turtle
#import keyboard
#from unittest import result
'''
约定第一行为标识，表示卡池
'''

lis=open("people.txt","r").readlines()

Card=lis[0]
lis.pop(0)
#print(lis)

def buttonPress():
    #input()
    p=random.randint(0,len(lis)-1)
    messagebox.showinfo("结果",lis[p])
    #print(lis[p])
    lis.pop(p)

def a10lianchou():
    peopleList=[]
    for i in range(10):
        p=random.randint(0,len(lis)-1)
        peopleList.append(lis[p])
        #print(lis[p])
        lis.pop(p)
    result=""
    for i in peopleList:
        result+=str(int(i))
        result+=" "
    messagebox.showinfo("结果",result)    

a=tkinter.Tk()
a.title("抽奖")
#a.geometry("200x100")
a.resizable(False,False)
a.attributes('-fullscreen', True) 
tkinter.Button(a,text="抽一次",command=buttonPress).pack()
tkinter.Button(a,text="十连抽",command=a10lianchou).pack()
tkinter.Button(a,text="Quit",command=exit).pack()
a.mainloop()

#turtle.onkeypress(a10lianchou,Space)
#turtle.mainloop()