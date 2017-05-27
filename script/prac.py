# -*- coding: utf-8 -*-
import urllib.request
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

def SearchFacility(name,Rlist):
    list = []
    url = "http://openAPI.seoul.go.kr:8088/4d4d49575973696c3131305472464d63/xml/SearchFacilityByIDService/1/5/"
    station = SearchStation(name,Rlist)
    inputnum = str(station.Getcode())
    if inputnum =='0':
        list.append("존재하지 않는 역입니다.")
        return list

    facility = urllib.request.urlopen(url+inputnum).read()
    facility = facility.decode('utf-8')

    facility = ET.fromstring(str(facility))
    elemet = facility.getiterator("row")

    for item in elemet:
        Lname = item.find("AREA_NM")
        list.append(Lname.text)
    return list



Rootlist = []
for i in range(4):
    temp = CreatRootList(i + 1)
    Rootlist.append(temp)

facility = SearchFacility('동두천',Rootlist)
for i in facility:
    print(i)