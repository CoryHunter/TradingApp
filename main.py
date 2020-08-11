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
    
class Sign_In_Page(Frame):
    
    def __init__(self, master = None):
        
        Frame.__init__(self, master)
        self.master = master
        
        self.log_in_window()
        
        
    def log_in_window(self):
        self.master.title("Cory's Trading App")
        self.configure(background = "#2C3531")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        height = screen_height//2
        width = screen_width//3
        x = (screen_width//2) - (width//2)
        y = (screen_height//2) - (height//2)
        self.master.geometry(str(width) +  'x' + str(height) + '+' + str(x) + '+' +str(y))
        self.pack(fill = BOTH, expand = 1)
        Instruction_Font = font.Font(family = "Gilroy-Medium", size = 40, weight = 'bold')
        Log_In = Button(self , text = "Log In", command = self.log_in, bg = "blue")
        Log_In.place(relx = .5, rely = .60, anchor = CENTER, relheight = .075, relwidth = .25)
        API_Key_Label = Label(self, text="API Key ID:", bg = "#2C3531" , fg = "#D1E8E2").place(relx = .05, rely = .30 )
        Secret_Key_Label = Label(self, text="Secret Key:", bg = "#2C3531", fg = "#D1E8E2").place(relx = .05, rely = .40 )
        Water_MArk_Label = Label(self, text = "Produced By Cory Hunter", bg = "#2C3531", fg = "#FFCB9A").place(relx = .995, rely = .995,anchor = SE)
        Instructions = Label(self, text = "Log In Using Alpaca Keys", bg = "#2C3531", fg = "#116466", font = Instruction_Font).place(relx = .5, rely = .15,anchor = CENTER)

        self.API_Key_Entry = Entry(self)
        self.Secret_Key_Entry = Entry(self)
    
        self.API_Key_Entry.place(relx = .35, rely = .30, relheight = .07, relwidth = .45)
        self.Secret_Key_Entry.place(relx = .35, rely = .40, relheight = .07, relwidth = .45)

        
    def log_in(self):
        self.API_Key = self.API_Key_Entry.get()
        self.Secret_Key = self.Secret_Key_Entry.get()
        
        try: 
            self.api = alpaca.REST(self.API_Key, self.Secret_Key, base_url = 'https://paper-api.alpaca.markets')
            self.account = self.api.get_account()
            self.root.destroy 
            
        except: 
            print("Failed Log In")
            self.log_in_failed()
            
    def log_in_failed(self):
        self.log_in_window()
        messagebox.showerror("Invalid Sign-In", "Make Sure Your Keys Correct and Try Again")
        
def run_app():
    root = Tk()
    app = Sign_In_Page(root)
    root.mainloop()

        
        

