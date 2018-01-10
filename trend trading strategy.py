#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:27:48 2017

@author: MAngO
"""
import numpy as np
import pandas as pd
# Here we use technical analysis functions written by ourselves. If you want to use
# packages like TA-Lib, you need to follow the installation guidance down below:
# https://mrjbq7.github.io/ta-lib/install.html
from auxiliary import generate_bar, rise_flag

''' You can define variables that your strategy may use during the backtesting process here
'''
bar_length = 10 # Number of minutes to generate next new bar, Trading frequency

asset_index = 0 # Index of asset you want to use in this strategy, e.g. AU


my_cash_balance_lower_limit = 3000000. 
ind=3
N=3
K1=0.5
K2=1.5


def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    ''' Params: timer = int, counter of current time
        data = pandas.dataframe, data for current minute bar
        info - pandas.dataframe, information matrix
        init_cash，transaction - double, constans
        detail_last_min - list, contains cash balance, margin balance, total balance and position of last minute
        memory - class, current memory of your strategy
    '''
    
    position_new = detail_last_min[0]# Get position of last minute
    
    
    
    if(timer==0):
    
        memory.data_list = list()
        memory.trade_times=0
    
        memory.long_stop_loss = np.inf
        memory.long_profit_target = np.inf
        memory.short_stop_loss = np.inf
        memory.short_profit_target = np.inf
        
        memory.range=np.inf
        memory.buyline=np.inf
        memory.selline=np.inf
        memory.data_list.append(data)
        memory.data_list=np.asarray(memory.data_list)
        memory.data_list=list(memory.data_list)
    
    if(timer%bar_length==0 and timer!=0):
        memory.data_list.append(data)
        memory.data_list=np.asarray(memory.data_list)
        last_close=memory.data_list[-1,ind,3]
    

        if len(memory.data_list)>N:
            HH=max(memory.data_list[-1*N:-2,ind,1])
            LL=min(memory.data_list[-1*N:-2,ind,2])
            LC=min(memory.data_list[-1*N:-2,ind,3])
            HC=max(memory.data_list[-1*N:-2,ind,3])
            memory.range=max(HH-LC,HC-LL)
            memory.buyline=memory.data_list[-2][ind][0]+K1*memory.range
            memory.selline=memory.data_list[-2][ind][0]-K2*memory.range
            print(last_close,memory.buyline,memory.selline)
            if last_close>memory.buyline:
                position_new[ind]+=100
                memory.trade_times+=1
                print("short position："+str(position_new[ind]))
            if last_close<memory.selline:
                position_new[ind]=0
                memory.trade_times+=1
                print("long position："+str(position_new[ind]))
            
           
        memory.data_list=list(memory.data_list)
    return position_new, memory
    
if __name__ == '__main__':
    ''' This strategy simply check if there is any special technical pattern in data
        No training process required. Main function is passed.
    '''
    pass