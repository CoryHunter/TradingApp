#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:43:37 2020

@author: coryhunter
"""

from tkinter import *
import webbrowser
import alpaca_trade_api as alpaca
from tkinter import font
from tkmacosx import Button
import yfinance as yf
import requests
import bs4 as bs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime as dt
from tkinter import ttk
import yfinance as yf
import random as rand





    
class Sign_In_Page(Frame):
    
    def __init__(self, master = None):
        
        Frame.__init__(self, master)
        self.master = master
        self.trade_window_setup()
        self.log_in_window()
        
    def save_sp500_dict(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        names= []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)
            names.append(row.findAll('td')[1].text)
        for i in range(len(tickers)):
            tickers[i] = tickers[i].strip()
        self.sp500_dictionary =  dict(zip(tickers,names))
        
            
        
    def log_in_window(self):
        self.sign_in = Toplevel()
        self.sign_in.title("Sign-In")
        self.sign_in.configure(background = "#303030")
        self.screen_width = self.sign_in.winfo_screenwidth()
        self.screen_height = self.sign_in.winfo_screenheight()
        height = 500
        width = 450
        x = (self.screen_width//2) - (width//2)
        y = (self.screen_height//2) - (height//2)
        self.sign_in.geometry(str(width) +  'x' + str(height) + '+' + str(x) + '+' +str(y))
        self.pack(fill = BOTH, expand = 1)
        Instruction_Font = font.Font(family = "Gilroy-Medium", size = 40)
        Label_Font = font.Font(family = "Gilroy-Medium", size = 20)
        Log_In = Button(self.sign_in , text = "Log In" , borderless=1, command = self.log_in)
        Log_In.place(relx = .5, rely = .60, anchor = CENTER, relheight = .075, relwidth = .25)
        Go_To_Alpaca = Button(self.sign_in , text = "Go to Alpaca", borderless=1, bg = '#FFD700', command = self.go_to_website)
        Go_To_Alpaca.place(relx = .5, rely = .73, anchor = CENTER, relheight = .075, relwidth = .25)
        API_Key_Label = Label(self.sign_in, text="API Key ID:", bg = "#303030" , fg = "#D1E8E2", font = Label_Font).place(relx = .05, rely = .30 )
        Secret_Key_Label = Label(self.sign_in, text="Secret Key:", bg = "#303030", fg = "#D1E8E2", font = Label_Font).place(relx = .05, rely = .40 )
        Water_Mark_Label = Label(self.sign_in, text = "Produced By Cory Hunter", bg = "#303030", fg = '#FFD700').place(relx = .995, rely = .995,anchor = SE)
        Instructions = Label(self.sign_in, text = "Log In Using Alpaca Keys", bg = "#303030", fg = 'white', font = Instruction_Font).place(relx = .5, rely = .15,anchor = CENTER)

        self.API_Key_Entry = Entry(self.sign_in, borderwidth = 0.5, relief = SUNKEN)
        self.Secret_Key_Entry = Entry(self.sign_in, borderwidth = 0.5, relief = SUNKEN)
    
        self.API_Key_Entry.place(relx = .35, rely = .30, relheight = .07, relwidth = .45)
        self.Secret_Key_Entry.place(relx = .35, rely = .40, relheight = .07, relwidth = .45)
        
        self.sign_in.attributes("-topmost", True)
        
        
    def trade_window_setup(self):
        self.save_sp500_dict()
        self.master.title("Cory's Trading App")
        self.configure(background = "#303030")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(str(screen_width) +  'x' + str(screen_height) + '+0+0')
        Header_Font = font.Font(family = "Gilroy-Medium", size = 60)
        Header = Label(self, text = "Trading Platform", bg = "#303030", fg= "white", font = Header_Font)
        Header.place(relx = .5, rely = .00001, anchor = N)
        Water_Mark_Label_Trade_Window = Label(self, text = "Produced By Cory Hunter", bg = "#303030", fg = '#FFD700').place(relx = .995, rely = .995,anchor = SE)
        
        
    def log_in(self):
        self.API_Key = self.API_Key_Entry.get()
        self.Secret_Key = self.Secret_Key_Entry.get()


        try:
            self.api = alpaca.REST(self.API_Key, self.Secret_Key, base_url = 'https://paper-api.alpaca.markets')
            self.account = self.api.get_account()
            self.finish_trade_window_setup()
            self.sign_in.destroy()
       
  
        except: 
            print("Failed Log In")
            self.log_in_failed()
       
            
    def get_company_from_ticker(self,ticker):
        try:
            return self.sp500_dictionary[ticker]
        except: 
            return ticker
            
        
    def go_to_website(self):
        webbrowser.open('https://alpaca.markets/')
        
    def go_to_website_and_close(self):
        
        webbrowser.open('https://alpaca.markets/')
        self.sign_in_error.destroy()
        
            
    def log_in_failed(self):
        self.sign_in_error = Toplevel()
        self.sign_in_error.title("Error")
        self.sign_in_error.configure(background = "#303030")
        center_x = (self.screen_width//2) - 150
        center_y = (self.screen_height//2) - 75
        self.sign_in_error.geometry('300x150+'+ str(center_x) + '+' +str(center_y))
        Header_Font = font.Font(family = "Gilroy-Medium", size = 15)
        Header = Label(self.sign_in_error, text = "Invalid keys, please use valid Alpaca Keys.", bg = "#303030", fg= "white", font = Header_Font)
        Closer_Error = Button(self.sign_in_error , text = "Close", borderless=1, command = self.sign_in_error.destroy)
        Closer_Error.place(relx = .35, rely = .85, anchor = CENTER)
        Open_Alpaca = Button(self.sign_in_error , text = "Go To Alpaca", borderless=1, command = self.go_to_website_and_close)
        Open_Alpaca.place(relx = .65, rely = .85, anchor = CENTER)
        Header.place(relx = .5, rely = .35, anchor = N)
        self.sign_in_error.attributes("-topmost", True)
        
    def graph_error(self):
        self.graph_error_box = Toplevel()
        self.graph_error_box.title("Error")
        self.graph_error_box.configure(background = "#303030")
        center_x = (self.screen_width//2) - 200
        center_y = (self.screen_height//2) - 100
        self.graph_error_box.geometry('400x200+'+ str(center_x) + '+' +str(center_y))
        Header_Font = font.Font(family = "Gilroy-Medium", size = 15)
        Header = Label(self.graph_error_box, text = self.graph_error_message, bg = "#303030", fg= "white", font = Header_Font)
        Closer_Error = Button(self.graph_error_box , text = "Close", borderless=1, command = self.graph_error_box.destroy)
        Closer_Error.place(relx = .5, rely = .85, anchor = CENTER)
        Header.place(relx = .5, rely = .35, anchor = N)
        self.graph_error_box.attributes("-topmost", True)
        
    def portfolio_graph(self):
        figure = plt.Figure(figsize=(6,5), dpi=100,facecolor='white',linewidth = 5, edgecolor='black')
        if self.asset_to_graph == "Entire Portfolio":
            self.asset_history = self.api.get_portfolio_history(timeframe= self.timeframe,period = self.period).df
        else: 
            self.asset_history = pd.DataFrame(yf.download(self.asset_to_graph, period = self.period, interval = self.timeframe))
        if self.timeframe[1] == 'M':
            self.asset_history.index = [dt.strptime(x.__str__()[11:19], '%H:%M:%S').time() for x in self.asset_history.index] 
        if self.period == '1D':
            const = self.api.get_portfolio_history(timeframe="1D",period ="1W").df.equity.iloc[-2]
            self.asset_history['Yesterdays_Close'] = pd.Series([const for x in range(len(self.asset_history.index))], index=self.asset_history.index)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self)
        chart_type.get_tk_widget().place(relx = .25 ,rely = .560, anchor = S, relwidth = .40, relheight = .46)
        if self.asset_to_graph == "Entire Portfolio":
            plot = self.asset_history.equity.plot( kind='line', legend=True, ax=ax)
        else:
            plot = self.asset_history.Close.plot(kind = 'line', legend = self.asset_to_graph, ax = ax)
        plot.set_facecolor('white')
        plot.spines['top'].set_visible(False)
        plot.spines['right'].set_visible(False)
        if self.period == '1D':
            self.asset_history.Yesterdays_Close.plot(kind='line', legend=True, ax=ax)
        ax.ticklabel_format(axis = 'y', style = 'plain',useOffset=False)
        ax.set_ylabel("USD")
        if self.asset_to_graph == "Entire Portfolio":
            ax.set_title(self.asset_to_graph)
            ax.legend(["Equity"])
        else:
            ax.set_title(self.get_company_from_ticker(self.asset_to_graph))
            ax.legend(["Price Per Share"])
        
        
    def position_box_update(self):
        
        self.Position_Font = font.Font(family = "Menlo", size = 20)
        self.position_box = Listbox(self, bg = "white", fg = "#303030", font = self.Position_Font, borderwidth = 5)
        self.scroll_positions = Scrollbar(self.position_box, orient = VERTICAL)
        self.position_box.config(yscrollcommand = self.scroll_positions.set)
        self.positions = self.api.list_positions()
        self.position_box.place(relx = .5 ,rely = .96, anchor = S, relwidth = .95, relheight = .20)
        labels = " Company"
        while (len(labels) < 28):
            labels = labels + " "
        labels = labels + "Ticker"
        while (len(labels) < 45):
            labels = labels + " "
        labels = labels + "Quantity"
        while (len(labels) < 60):
            labels = labels + " " 
        labels = labels + "Avg. Price"
        while (len(labels) < 80):
            labels = labels + " "
        labels = labels + "Current Price"
        while (len(labels) < 100):
            labels = labels + " "
        labels = labels + "Equity"
        self.Position_Labels = Label(self, text = labels, bg = '#303030' , fg = "white",  font = self.Position_Font)
        self.Position_Labels.place(relx = .47, rely = .755, anchor = S)
        for i in range(len(self.positions)):
            temp = " " + self.get_company_from_ticker(self.positions[i].symbol)
            if (len(temp) > 25):
                temp = temp[:22] + "...   "
            else:
                while (len(temp) < 28):
                       temp = temp + " "
            temp = temp + self.positions[i].symbol
            while (len(temp) < 45):
                temp = temp + " "
            temp = temp + self.positions[i].qty
            while (len(temp) < 60):
                temp = temp + " " 
            temp = temp + self.positions[i].avg_entry_price
            while (len(temp) < 80):
                temp = temp + " "
            temp = temp + self.positions[i].current_price
            while (len(temp) < 100):
                temp = temp + " "
            temp = temp + self.positions[i].market_value
            self.position_box.insert(i,temp)
            if (float(self.positions[i].current_price)>float(self.positions[i].avg_entry_price)):
                self.position_box.itemconfig(i,fg = "green")
            elif (float(self.positions[i].current_price) == float(self.positions[i].avg_entry_price)):
                pass
            else:
                self.position_box.itemconfig(i,fg = "red") 
        
        self.scroll_positions.config(command = self.position_box.yview)
        
        self.scroll_positions.pack(side = RIGHT, fill = Y)
        
    def refresh_graph(self):
        temp_bool = True
        self.asset_to_graph = self.asset_option.get()
        if self.asset_to_graph == "Entire Portfolio":
            self.timeframe = self.timeframe_option.get()
            if self.timeframe == "1 Minute":
                self.timeframe = "1Min"
            elif self.timeframe == "5 Minute":
                self.timeframe = "5Min"
            elif self.timeframe == "15 Minute":
                self.timeframe = "15Min"
            else:
                self.timeframe = "1D"   
            self.period = self.period_option.get()
            if self.period == 'Today':
                self.period = "1D"
            elif self.period == '1 Week':
                self.period = "1W"
            elif self.period == '1 Month':
                self.period = "1M"
            elif self.period == '3 Months':
                self.period = "3M"
        else:
            self.timeframe = self.timeframe_option.get()
            if self.timeframe == "1 Minute":
                self.timeframe = "1m"
            elif self.timeframe == "5 Minute":
                self.timeframe = "5m"
            elif self.timeframe == "15 Minute":
                self.timeframe = "15m"
            else:
                self.timeframe = "1d"   
            self.period = self.period_option.get()
            if self.period == 'Today':
                self.period = "1d"
            elif self.period == '1 Week':
                self.period = "7d"
            elif self.period == '1 Month':
                self.period = "1mo"
            elif self.period == '3 Months':
                self.period = "3mo"
        if self.timeframe != ("1D" and "1d"):
            if self.period != ("1D" and "1d"):
                self.graph_error_message = self.timeframe_option.get() + " must be used with period \"Today\"" 
                self.graph_error()
                temp_bool = False
        if self.timeframe == ("1D" and "1d"):
            if self.period == ("1D" and "1d"):
                self.graph_error_message = self.timeframe_option.get() + " can\'t be used with period \"Today\"" 
                self.graph_error()
                temp_bool = False
        if temp_bool:
            self.portfolio_graph()
        
    def insert_graph_options(self):
        symbols = [position.symbol for position in self.positions]
        symbols.insert(0,"Entire Portfolio")
        self.asset_option = ttk.Combobox(self, width = 15, values = symbols)
        self.asset_option.place(relx = .35, rely = .59, anchor = CENTER)
        self.timeframe_option = ttk.Combobox(self, width = 15, values = ['1 Minute','5 Minute','15 Minute', '1 Day'])
        self.timeframe_option.place(relx = .35, rely = .635, anchor = CENTER)
        self.period_option = ttk.Combobox(self, width = 15, values = ['Today','1 Week', '1 Month','3 Months'])
        self.period_option.place(relx = .35, rely = .68, anchor = CENTER)
        self.refresh_graph = Button(self , text = "Refresh Graph" , borderless=1, command = self.refresh_graph)
        self.refresh_positions = Button(self , text = "Refresh Positions" , borderless=1, command = self.position_box_update)
        self.refresh_graph.place(relx = .12, rely = .60, anchor = CENTER, relheight = .05, relwidth = .1)
        self.refresh_positions.place(relx = .12, rely = .67, anchor = CENTER, relheight = .05, relwidth = .1)
        self.Asset_Option = Label(self, text = "Asset:", bg = '#303030' , fg = "white",  font = self.Position_Font)
        self.Asset_Option.place(relx = .28, rely = .59, anchor = E)
        self.Timeframe_Option = Label(self, text = "TimeFrame:", bg = '#303030' , fg = "white",  font = self.Position_Font)
        self.Timeframe_Option.place(relx = .28, rely = .635, anchor = E)
        self.Period_Option = Label(self, text = "Period:", bg = '#303030' , fg = "white",  font = self.Position_Font)
        self.Period_Option.place(relx = .28, rely = .68, anchor = E)
        
    def start_new_strategy(self):
        self.Testing_Label = Label(self, text = self.trading_option.get())
        self.Testing_Label.place(relx = .75, rely = .35, anchor = CENTER)
        
    def init_trade_functions(self):
        self.trading_option = ttk.Combobox(self, values = ["Moving Average Method","Upswing Method","Robinhood Notification Method", "Stop All Methods"])
        self.trading_option.place(relx = .81, rely = .635, anchor = CENTER, relwidth = .25)
        self.start_trading = Button(self, text = "Start Trading", borderless = 1, command = self.start_new_strategy)
        self.start_trading.place(relx = .6, rely = .635, anchor = CENTER, relheight = .05, relwidth = .1)
        self.trading_strategy_descriptions = Listbox(self, bg = "white", fg = "#303030", font = self.Position_Font, borderwidth = 3)
        self.trading_strategy_descriptions.insert(1," MOVING AVERAGE METHOD: This method takes a")
        self.trading_strategy_descriptions.insert(2," moving average and buys when the the moving")
        self.trading_strategy_descriptions.insert(3," average is goes from above the current price")
        self.trading_strategy_descriptions.insert(4," and then sells when it goes below the ")
        self.trading_strategy_descriptions.insert(5," moving average.")
        self.trading_strategy_descriptions.insert(6,"")
        self.trading_strategy_descriptions.insert(7," UPSWING METHOD: This method looks for then")
        self.trading_strategy_descriptions.insert(8," the stock price is going down and then")
        self.trading_strategy_descriptions.insert(9," starts to swing back up. It will buy once")
        self.trading_strategy_descriptions.insert(10," it starts to swing back up and then quickly ")
        self.trading_strategy_descriptions.insert(11," sell to capture small but fast profits.")
        self.trading_strategy_descriptions.insert(12," (COMMITS DAYTRADES)")
        self.trading_strategy_descriptions.insert(13,"")
        self.trading_strategy_descriptions.insert(14," ROBINHOOD METHOD: This method monitors")
        self.trading_strategy_descriptions.insert(15," notifications given from Robinhood. It buys")
        self.trading_strategy_descriptions.insert(16," when there is a notification loss of 5 or")
        self.trading_strategy_descriptions.insert(17," more percent and sells at the end of the day.")
        self.trading_strategy_descriptions.insert(18," (COMMITS DAYTRADES)")
        self.trading_strategy_descriptions.insert(19,"")
        self.trading_strategy_descriptions.insert(20,"")
        self.trading_strategy_descriptions.place(relx = .75 ,rely = .560, anchor = S, relwidth = .40, relheight = .46)
        self.scroll_strategies = Scrollbar(self.trading_strategy_descriptions, orient = VERTICAL)
        self.trading_strategy_descriptions.config(yscrollcommand = self.scroll_strategies.set)
        self.scroll_strategies.config(command = self.trading_strategy_descriptions.yview)
        self.scroll_strategies.pack(side = RIGHT, fill = Y)
        
        
    def finish_trade_window_setup(self):
        self.position_box_update()  
        self.timeframe = "1Min"
        self.period = "1D"
        self.asset_to_graph = "Entire Portfolio"
        self.portfolio_graph()
        self.insert_graph_options()
        self.init_trade_functions()
        
        
        
def run_app():
    root = Tk()
    app = Sign_In_Page(root)
    root.mainloop()

        
        

