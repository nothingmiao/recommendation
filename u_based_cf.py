#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 20:23:58 2016

@author: wm
"""

from __future__ import division
import numpy
import time
rate={}#user:rate1(item1) rate2(item2)
item_dic={}#user:item1 item2
dic = {}#item:user1 user2
all_simi={}#user
all_simi_item={}#item
all_item=[]
def user_base(fname,out_name):
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    f1 = open(fname,'r')
    o = open(out_name,'w')
    current_user = '0'
    context = ''
    rating=[]   
    for line in f1:
        data1 = line.split('::')
        user1 = data1[0]
        item = data1[1]
        if user1 == current_user:
            context += item +' '
            rating.append(data1[2])
        elif current_user!='0':
            context += '\n'
            o.write(context)   
            rate[str(current_user)]=numpy.asarray([int(i) for i in rating])
            rating=[]
            context = user1 + ' : '+item +' '
            rating.append(data1[2])           
            current_user = user1           
        else:
            context = user1 + ' : '+item +' '
            rating.append(data1[2])
            current_user = user1
    rate[str(user1)]=numpy.asarray([int(i) for i in rating])
    o.write(context)  
    f1.close()
    o.close()
    
    f2=open(out_name,'r')
    count=0   
    for line in f2:
        data2 = line.split(' ')
        user2=data2[0]
        item_dic[str(user2)]=numpy.asarray([int(i) for i in data2[2:-1]])
        count+=1
    f2.close()
    
    f3=open(out_name,'r')   
    ww=0
    for line in f3:
        data3 = line.split(' ')
        user3=data3[0]
        simi=[]
        item_set1=set(item_dic[str(user3)])
        for i in range(1,count+1):
            item_set2=set(item_dic[str(i)])
            simi.append([len(item_set1&item_set2)/len(item_set1|item_set2),str(i)])
        a=sorted(simi,reverse = True)
        all_simi[user3]=numpy.asarray([i for i in a])    
        ww+=1
        if ww==10:
            break            
    f3.close()    
    
    f4=open('../ml-1M/1m_test_8','r')
    sumerr=0
    cou=0
    ww=0
    user_now='0'
    for line in f4:
        data4 = line.split('::')
        user4 = data4[0]
        item4 = data4[1]
        rating4 = data4[2]
        rate_test=0
        stop=0
        for i in all_simi[user4]: 
            k=0
            for j in item_dic[str(i[1])]:
                if str(j)==str(item4):  
                    rate_test=rate[str(i[1])][k]
                    stop=1
                    break
                else:
                    k+=1
            if stop==1:
                break
        if rate_test==0:
            rate_test=3
        #print rate_test,'~~~~~~~~',rating4
        sumerr+=(int(rate_test)-int(rating4))*(int(rate_test)-int(rating4))
        cou+=1
        
        if user_now!=user4:
            user_now=user4
            ww+=1
        if ww==9:
            break          
        #break
    f4.close()  
    print sumerr,cou
    rmse=numpy.sqrt(sumerr/cou)
    print 'RMSE:',rmse
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
