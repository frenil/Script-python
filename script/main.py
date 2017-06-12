# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
import ReadAPI

window = Tk()
window.geometry("800x600+400+200")

def InitRenderText():
    global RenderText
    TempFont = font.Font(window, size=10, family='Consolas')
    RenderText = Text(window, width=90, height=20, borderwidth=12, relief='ridge')
    RenderText.pack()
    RenderText.place(x=50, y=250)
    RenderText.configure()

def GetEntry():
    global start
    global dest
    global findstation
    global station
    start = Entry(window)
    dest = Entry(window)
    findstation = Entry(window)
    station = Entry(window)
    start.place(x = 70,y=110)
    dest.place(x = 70,y=160)
    findstation.place(x=350, y=110)
    station.place(x = 630,y=110)

def Realtime():
    global stationtime
    global RenderText
    global station
    up,down = ReadAPI.RealTimeArrive(station.get())
    RenderText.delete(0.0, END)

    if up!=None:
        RenderText.insert(INSERT, "상행")
        RenderText.insert(INSERT, "열차 도착시간은 ")
        RenderText.insert(INSERT, str(up))
        RenderText.insert(INSERT, "입니다.")
        RenderText.insert(INSERT, "\n")
    else:
        RenderText.insert(INSERT, "상행 정보가 없습니다.")
        RenderText.insert(INSERT, "\n")
    if down!=None:
        RenderText.insert(INSERT, "하행")
        RenderText.insert(INSERT, "열차 도착시간은 ")
        RenderText.insert(INSERT, str(down))
        RenderText.insert(INSERT, "입니다.")
        RenderText.insert(INSERT, "\n")
    else:
        RenderText.insert(INSERT, "하행 정보가 없습니다.")
        RenderText.insert(INSERT, "\n")
    if up==None and down==None:
        RenderText.insert(INSERT, "입력값이 잘못되거나 정보가 없을 수 있습니다.")
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "다음 열차가 10분 이상 남있을 경우 데이터가 없을 수 있습니다")

def Getbutton():
    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    b1 = Button(window, font = TempFont,text="경로 검색",command = SearchRoot)
    b1.place(x = 50,y=200)
    b2 = Button(window, font = TempFont,text="시설 검색",command = SearchFacility)
    b2.place(x = 330,y=200)

    b3 = Button(window, font = TempFont,text="시간 검색",command = Realtime)
    b3.place(x = 600,y=200)
    return b1

def drawInit():
    TempFont = font.Font(window, size=20, weight='bold', family='Consolas')
    MainText = Label(window, font=TempFont, text="[서울시 지하철역 검색 App]")
    MainText.pack()
    MainText.place(x=200)
    FirstText = Label(window, font=TempFont, text="경로 검색")
    FirstText.pack()
    FirstText.place(x=20,y=50)

    SecondText = Label(window, font=TempFont, text="시설물 검색")
    SecondText.pack()
    SecondText.place(x=300, y=50)

    ThirdText = Label(window, font=TempFont, text="열차 도착시간")
    ThirdText.pack()
    ThirdText.place(x=580, y=50)
    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    start = Label(window, font=TempFont,text="출발역")
    start.place(y=110)
    destination = Label(window, font=TempFont, text="도착역")
    destination.place(y=160)

    find = Label(window, font=TempFont, text="역검색")
    find.place(x = 280,y=110)
    ps = Label(window, font=TempFont, text="1~9호선 까지검색가능")
    ps.place(x = 280,y= 140)
    ps2 = Label(window, font=TempFont, text="URL문제로 2호선 검색 불가")
    ps2.place(x=280, y=170)
    real = Label(window, font=TempFont, text="역검색")
    real.place(x=550, y=110)

def GetStationList(line):
    list = []
    list.append(ReadAPI.CreatRootList(line))
    return list

def SearchFacility():
    global Rootlist
    global findstation
    global RenderText
    facility = ReadAPI.SearchFacility(str(findstation.get()), Rootlist)
    RenderText.delete(0.0, END)
    if facility:
        RenderText.insert(INSERT,  findstation.get()+"역의 주요시설은")
        RenderText.insert(INSERT, "\n")
        for i in facility:
            RenderText.insert(INSERT,i)
            RenderText.insert(INSERT,"\n")
        RenderText.insert(INSERT,"가 있습니다.")
        left, right = ReadAPI.SearchNear(findstation.get(), Rootlist)
        RenderText.insert(INSERT, "\n")

        if left.Getname()!=0:
            RenderText.insert(INSERT,"이전역은 "+left.Getname()+"입니다.")
            RenderText.insert(INSERT, "\n")
        if right.Getname()!=0:
            RenderText.insert(INSERT,"다음역은 "+ right.Getname()+"입니다.")
    else:
        RenderText.insert(INSERT, "정보가 없거나 잘못된 입력입니다.")

def SearchRoot():
    global start
    global dest
    global RenderText
    result = ReadAPI.SearchRout(str(start.get()),str(dest.get()))
    RenderText.delete(0.0, END)
    if result:
        RenderText.insert(INSERT,str(start.get()))
        RenderText.insert(INSERT,"역 출발 ")
        RenderText.insert(INSERT,result)
        RenderText.insert(INSERT,"에서 환승 ")
        RenderText.insert(INSERT,str(dest.get()))
        RenderText.insert(INSERT,"역 도착")
    else:
        RenderText.insert(INSERT, "잘못된 입력입니다.")

def main():
    global Rootlist

    drawInit()
    InitRenderText()
    GetEntry()
    button1 = Getbutton()
    Rootlist = ReadAPI.insertLine()
    print(Rootlist)
    window.mainloop()

main()