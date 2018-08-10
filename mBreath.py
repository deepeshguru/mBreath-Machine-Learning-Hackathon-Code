# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 23:16:38 2018

@author: Deepesh Agrawal
"""

#----------------part 1---------------------------------------------

import xml.etree.ElementTree as ET
import csv
import pandas as pd
import numpy as np

tree = ET.parse("data-20180808T130213Z-001\data\apnea\mesa-sleep-0001-profusion.xml")
root = tree.getroot()

# open a file for writing

mesa_data = open('mesa_sleep_xml.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(mesa_data)
mesa_head = []

count = 0
for member in root.findall('ScoredEvents'):
    for members in member.findall('ScoredEvent'):
        scoredevent = []
        if count == 0:
            Duration = members.find('Duration').tag
            mesa_head.append(Duration)
            Input = members.find('Input').tag
            mesa_head.append(Input)
            Name = members.find('Name').tag
            mesa_head.append(Name)
            Start = members.find('Start').tag
            mesa_head.append(Start)
            csvwriter.writerow(mesa_head)
            count = count + 1
        Duration = members.find('Duration').text
        scoredevent.append(Duration)
        Input = members.find('Input').text
        scoredevent.append(Input)
        Name = members.find('Name').text
        scoredevent.append(Name)
        Start = members.find('Start').text
        scoredevent.append(Start)
        csvwriter.writerow(scoredevent)
mesa_data.close()
mesa_data = pd.read_csv("mesa_sleep_xml.csv")
mesa_data.to_csv('mesa_sleep_xml.csv',index=0)




#---------------------------------part 2------------------------------------------
import pyedflib

f = pyedflib.EdfReader("data-20180808T130213Z-001\data\flow\mesa-sleep-0001.edf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))


try:
    
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
except:
    print(" ")


Flow = np.transpose(sigbufs[0,:])
Epoch = [0]*len(Flow)
for i in range(len(Flow)):
    Epoch[i] = i/32


mesa_sleep_edf = pd.DataFrame({"Epoch":Epoch, "Flow":Flow})

mesa_sleep_edf.to_csv("mesa_sleep_edf.csv", index = 0)





#-----------------------------part 3------------------------------

tree = ET.parse("data-20180808T130213Z-001\data\stage\mesa-sleep-0001-nsrr.xml")
root = tree.getroot()

# open a file for writing

mesa_data_nsrr = open('mesa_sleep_nsrr.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(mesa_data_nsrr)
mesa_head_nsrr = []

count = 0
for member in root.findall('ScoredEvents'):
    for members in member.findall('ScoredEvent'):
        scoredevent = []
        if count == 0:
            Duration = members.find('Duration').tag
            mesa_head_nsrr.append(Duration)
            Stages = members.find('EventConcept').tag
            mesa_head_nsrr.append(Stages)
            Start = members.find('Start').tag
            mesa_head_nsrr.append(Start)
            Type = members.find('EventType').tag
            mesa_head_nsrr.append(Type)
            csvwriter.writerow(mesa_head_nsrr)
            count = count + 1
        Duration = members.find('Duration').text
        scoredevent.append(Duration)
        Stages = members.find('EventConcept').text
        scoredevent.append(Stages)
        Start = members.find('Start').text
        scoredevent.append(Start)
        Type = members.find('EventType').text
        scoredevent.append(Type)
        csvwriter.writerow(scoredevent)
mesa_data_nsrr.close()
mesa_sleep_nsrr = pd.read_csv("mesa_sleep_nsrr.csv")
mesa_sleep_nsrr.rename(columns={'Duration': 'Duration', 'EventConcept': 'Stages', 'Start': 'Start', 'EventType': 'Type'}, inplace=True)

mesa_sleep_nsrr.to_csv('mesa_sleep_nsrr.csv',index=0)



#-----------------------------------part 4 -------------------------------------------

a = pd.read_csv("mesa_sleep_edf.csv")
b = pd.read_csv("mesa_sleep_xml.csv")
c = pd.read_csv("mesa_sleep_nsrr.csv")

combined = pd.concat([a,b,c],sort = True)

combined = combined[['Epoch','Flow','Name','Stages']]


combined.rename(columns={'Epoch': 'Time', 'Flow': 'Flow', 'Name': 'Name', 'Stages': 'Stages'}, inplace=True)

combined = combined1.fillna(0)

combined.to_csv("mesa_sleep.csv",index=0)


