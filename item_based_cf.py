# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 09:34:31 2016

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
    
def item_base(fname,out_name):
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    f6 = open(fname,'r')
    o1 = open(out_name,'w')
    
    for line in f6:
        data = line.split('::')
        user = data[0]
        item = data[1]
        
        if not (dic.has_key(item)):
            dic[item]=[]
            all_item.append(item)
            dic[item].append(user)
        else:
            dic[item].append(user)
    
    for item,users in dic.items():
        o1.write(item+' : ')
        for user in users:
            o1.write(user+' ')
        o1.write('\n')
    f6.close()
    o1.close() 
    #ww=0
    for i,users in dic.items():
        #print i
        simi=[]
        item_set1=set(dic[i])
        for j in all_item:
            if str(j)!=str(i):
                item_set2=set(dic[str(j)])
                simi.append([len(item_set1&item_set2)/len(item_set1|item_set2),j])
        a=sorted(simi,reverse = True)
        all_simi_item[i]=numpy.asarray([k for k in a])   
    f5=open('../ml-1M/1m_test_8','r')
    sumerr2=0
    cou2=0
    #ww=0
    qq=0
    bb=0
    #user_now='0'
    for line in f5:
        data4 = line.split('::')
        user4 = data4[0]
        item4 = data4[1]
        rating4 = data4[2]
        rate_test2=0
        if all_simi_item.has_key(item4):
            aa=0
            stop=0
            for i in all_simi_item[item4]: 
                k=0
                aa+=1
                for j in item_dic[user4]:                    
                    if str(j)==str(i[1]):
                        bb+=1
                        rate_test2=rate[user4][k]
                        stop=1
                        break
                    else:
                        k+=1
                if stop==1:
                    break
        if rate_test2==0:
            qq+=1
            rate_test2=3
        #print rate_test2,'~~~~~~~~',rating4
        sumerr2+=(int(rate_test2)-int(rating4))*(int(rate_test2)-int(rating4))
        cou2+=1
    f5.close()  
    print 'not predict:',qq,'predict:',bb
    print sumerr2,cou2
    rmse2=numpy.sqrt(sumerr2/cou2)
    print 'RMSE:',rmse2
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))