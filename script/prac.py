# -*- coding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree as ET
import operator
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

    def Setname(self,name):
        self.name = name
    def Setnum(self,num):
        self.num = num
    def Setcode(self,code):
        self.code = code
    def Getname(self):
        return self.name
    def Getnum(self):
        return self.num
    def Getcode(self):
        return self.code

def CreatRootList(num):

    Rooturl = "http://openapi.seoul.go.kr:8088/646e4e417173696c37327874667077/xml/SearchSTNBySubwayLineService/1/999/"
    cnum = str(num)
    temp = Rooturl+cnum
    line = urllib.request.urlopen(temp).read()
    line = line.decode('utf-8')
    line = ET.fromstring(str(line))
    list = []
    elemet = line.getiterator("row")

    for item in elemet:
        Lname = item.find("STATION_NM")
        Lnum = item.find("LINE_NUM")
        Lcode = item.find("FR_CODE")
        list.append(station(Lname.text,Lnum.text, Lcode.text))
    return list


list = []
for i in range(4):
    temp = CreatRootList(i + 1)
    list.append(temp)
searchname = "소요산"
tempstation = station(0,0,0)
for d in list:
    for i in d:

        if i.Getname() in searchname:
            tempstation.copy(i)
            print("OK")
            break
print(tempstation.Getcode())