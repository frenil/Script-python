# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
from urllib.parse import quote
import xml.etree.ElementTree as ET
from xml.dom.minidom import *


class station:
    name= 'default name'
    num = -1
    code = 'default code'
    def __init__(self,iname,inum,icode):
        self.name = iname
        self.num = inum
        self.code = icode
    def copy(self,temp):
        self.name = temp.Getname()
        self.num = temp.Getnum()
        self.code = temp.Getcode()
    def Getname(self):
        return self.name
    def Getnum(self):
        return self.num
    def Getcode(self):
        return self.code
class Rout:
    start = None
    destination = None
    def __init__(self,start,des):
        self.start = start
        self.destination = des

def SearchRout(start,destination):
    list = []
    url = "http://swopenapi.seoul.go.kr/api/subway/455a6e764b73696c333959786a754d/xml/shortestRoute/0/5/"
    url2 = urllib.parse.quote_plus(start)
    url3 = urllib.parse.quote_plus(destination)
    temp = url +url2 +'/'+ url3

    rout = urllib.request.urlopen(temp).read()
    rout = rout.decode('utf-8')

    rout = ET.fromstring(str(rout))

    success = rout.getiterator("RESULT")
    isSuccess = None
    for i in success:
        isSuccess =i.find("code")

    if isSuccess.text == 'INFO-000':
        IDlist = None
        Namelist = None

        elemet = rout.getiterator("row")

        for i in elemet:
            IDlist = i.find("shtStatnId")
            Namelist = i.find("shtStatnNm")
            IDlist = IDlist.text.split(",")
            Namelist = Namelist.text.split(",")
            break
        for i in range(len(Namelist)):
            Namelist[i] = Namelist[i].replace(" ","")
        IDlist.pop()
        beforeID = int(IDlist[0])//1000000
        changeName = []
        for i in range(0, len(IDlist)):

            ID = int(IDlist[i]) // 1000000
            if ID != beforeID:
                print("환승")
                if ID<1010:
                    LineNum = str(ID-1000)+"호선"
                elif ID == 1061:
                    LineNum = "경의중앙선"
                elif ID == 1063:
                    LineNum = "중앙선"
                elif ID == 1065:
                    LineNum = "공항선"
                elif ID == 1067:
                    LineNum = "경춘선"
                elif ID == 1069:
                    LineNum = "인천1호선"
                elif ID == 1071:
                    LineNum = "수인선"
                elif ID == 1075:
                    LineNum = "분당선"
                elif ID == 1077:
                    LineNum = "신분당선"
                elif ID == 1078:
                    LineNum = "인천2호선"
                elif ID == 1079:
                    LineNum = "의정부경전철"
                elif ID == 1080:
                    LineNum = "용인경전철"
                else:
                    return False
                changeName.append((Namelist[i],LineNum))
            beforeID = ID
        return changeName
    elif isSuccess.text == 'INFO-200':
        return False

    return list

def CreatRootList(num):
    list = []

    Rooturl = "http://openapi.seoul.go.kr:8088/646e4e417173696c37327874667077/xml/SearchSTNBySubwayLineService/1/999/"
    cnum = str(num)
    temp = Rooturl+cnum

    line = urllib.request.urlopen(temp).read()
    line = line.decode('utf-8')
    line = ET.fromstring(str(line))
    elemet = line.getiterator("row")

    for item in elemet:
        Lname = item.find("STATION_NM")
        Lnum = item.find("LINE_NUM")
        Lcode = item.find("STATION_CD")
        list.append(station(Lname.text,Lnum.text, Lcode.text))
    return list
def SearchStation(name,list):
    tempstation = station(0, 0, 0)
    for d in list:
        for i in d:
            if i.Getname() == name:
                tempstation.copy(i)
                break
    return tempstation
def SearchNear(name,list):
    leftstation = station(0, 0, 0)
    rightstation = station(0,0,0)
    isFind = False
    for d in list:
        if isFind:
            break
        for i in d:
            if isFind:
                rightstation.copy(i)
                break

            if i.Getname() == name:
                isFind = True
            else:
                leftstation.copy(i)

    return leftstation, rightstation
def SearchFacility(name,Rlist):
    list = []
    url = "http://openAPI.seoul.go.kr:8088/4d4d49575973696c3131305472464d63/xml/SearchFacilityByIDService/1/5/"

    station = SearchStation(name,Rlist)
    inputnum = str(station.Getcode())

    if inputnum =='0':
        print("존재하지 않습니다.")
        list.append(0)
        return 0

    facility = urllib.request.urlopen(url+inputnum).read()
    facility = facility.decode('utf-8')

    facility = ET.fromstring(str(facility))
    elemet = facility.getiterator("row")

    for item in elemet:
        Lname = item.find("AREA_NM")
        list.append(Lname.text)
    return list
def PrintStation(name,facility, left,right):
    print(name+"역의 주요시설은")
    for i in facility:
        print(i)
    print("가 있습니다.")
    if left.Getname()!=0:
        print("이전역은 "+left.Getname()+"입니다.")
    if right.Getname()!=0:
        print("다음역은 "+ right.Getname()+"입니다.")
def insertLine():
    Rootlist = []

    for i in range(9):
        temp = CreatRootList(i + 1)
        Rootlist.append(temp)
    temp = CreatRootList("A")
    Rootlist.append(temp)
    temp = CreatRootList("B")
    Rootlist.append(temp)
    temp = CreatRootList("E")
    Rootlist.append(temp)
    temp = CreatRootList("G")
    Rootlist.append(temp)
    temp = CreatRootList("I")
    Rootlist.append(temp)
    temp = CreatRootList("I2")
    Rootlist.append(temp)
    temp = CreatRootList("K")
    Rootlist.append(temp)
    temp = CreatRootList("KK")
    Rootlist.append(temp)
    temp = CreatRootList("S")
    Rootlist.append(temp)
    temp = CreatRootList("SU")
    Rootlist.append(temp)
    temp = CreatRootList("U")
    Rootlist.append(temp)
    return Rootlist

isEnd = False
def main():
    Rootlist = insertLine()

    while isEnd !=True:
        searchtype = input("무엇을 하시겠습니까? (1:경로검색, 2:지하철역 정보, q:프로그램 종료): ")
        if searchtype == '1':
            start = input("출발 역을 입력하십시오: ")
            destination = input("도착 역을 입력하십시오: ")
            result = SearchRout(start,destination)
            if result==False:
                print("잘못된 입력입니다.")
            else:
                print(start+"역에서 출발 ",result, "환승  "+destination+"역에 도착")

        elif searchtype =='2':
            findname = input("검색할 역을 입력하시오: ")

            facility = SearchFacility(str(findname),Rootlist)
            if facility != 0 :
                left,right = SearchNear(findname,Rootlist)
                PrintStation(findname,facility,left,right)
        elif searchtype == 'q':
            print("이용해주셔서 감사합니다.")
            break
        else:
            print("잘못된 명령어입니다.")


main()