# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:10:32 2016

@author: wm
"""
from __future__ import division
import random
import math
import time
def SVD(factorNum,regularization,learningRate,iterTimes):
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    f1=open('../ml-1M/1m','r')
    user_set=set()
    item_set=set()
    user_num=0
    item_num=0
    dif={}
    for line in f1:
        data = line.split('::')
        user = data[0]
        item = data[1]
        #rating = data[2]
        if user not in user_set:
            user_set.add(user)
            user_num+=1
        if item not in item_set:
            item_set.add(item)
            item_num+=1
            dif[item]=int(item)-item_num+1
    print 'user number:',user_num,'item number:',item_num
    f1.close
    #初始化
    bu=[0.0 for i in range(user_num)]
    bi=[0.0 for i in range(item_num)]
    temp=math.sqrt(factorNum) #factorNum特征维数
    pu=[[(0.1*random.random()/temp) for i in range(factorNum)] for j in range(user_num)] #P、Q初始化，每个元素
    qi=[[0.1*random.random()/temp for i in range(factorNum)] for j in range(item_num)]

    f2=open('../ml-1M/1m_train_10','r')
    av=0.0
    summ=0.0
    count=0
    for line in f2:
        data = line.split('::')
        rating = int(data[2])
        count+=1
        summ+=rating
    av=summ/count
    f2.close
    print 'average rating:',av
    #train
    prermse=1000.0
    c=0
    for iter in range(iterTimes):
        f3=open('../ml-1M/1m_train_10','r')
        for line in f3:
            data=line.split('::')
            user = int(data[0])-1
            item = data[1]
            t=int(item)-int(dif[item])
            item=t
            rating = int(data[2])
            score=0.0
            for i in range(factorNum):
                score+=pu[user][i]*qi[item][i]
            predict_rating=av+bu[user]+bi[item]+score
            if predict_rating<1:
                predict_rating=1
            if predict_rating>5:
                predict_rating=5
            err=rating-predict_rating
            #update bu,bi
            bu[user]+=learningRate*(err-regularization*bu[user])
            bi[item]+=learningRate*(err-regularization*bi[item])
            #update pu,qi
            for k in range(factorNum):
                temp=qi[item][k]
                qi[item][k]+=learningRate*(err*pu[user][k]-regularization*qi[item][k])
                pu[user][k]+=learningRate*(err*temp-regularization*pu[user][k])               
        f3.close
        #test
        f4=open('../ml-1M/1m_test_10','r')
        summ=0.0
        count=0
        for line in f4:
            data=line.split('::')
            user = int(data[0])-1
            item = data[1]
            t=int(item)-int(dif[item])
            item=t
            rating = int(data[2])
            score=0.0
            for i in range(factorNum):
                score+=pu[user][i]*qi[item][i]
            predict_rating=av+bu[user]+bi[item]+score
            if predict_rating<1:
                predict_rating=1
            if predict_rating>5:
                predict_rating=5
            summ+=math.pow(rating-predict_rating,2)
            count+=1
        rmse=math.sqrt(summ/count)
        f4.close
        print "Iteration %d times,RMSE is : %f" % (iter+1,rmse)    
        if rmse>prermse:
            c+=1
        prermse=rmse
        if c==3:
            break
        #learningRate=learningRate*0.95
    print "Iteration finished!"
    print summ,count
    print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
SVD(100,0.05,0.02,100)