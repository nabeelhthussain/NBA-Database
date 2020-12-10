#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 21:51:28 2020

@author: nabeelhussain
"""
import pymysql
import tkinter as tk
import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

LARGE_FONT = ("Verdana", 12)
LARGEST_FONT = ("Verdana", 18)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("NBA Database System")
        self.geometry("1000x1000")
 
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {} # these are pages we want to navigate to
 
        for F in (StartPage, PageOne, CreatePage, ReadDraftPage, AddCollegePage, CreateStatsPage, ReadPage, ReadStadiumPage,UpdatePage, UpdateStatsPage, DeletePage): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
 
        self.show_frame(StartPage) # first page is StartPage
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
 
    def validateLogin(self, username, password, PageOne):
        global u,p
        u = username.get()
        p = password.get()
        print('Trying to connect')
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        print('Connected')
        self.show_frame(PageOne)
        return
    
    def get_task(self, choice):
        if choice.get() not in ['1','2','3','4','5','6','7']:
            tkinter.messagebox.showerror('ERROR','Option does not exist. Try again')
        else:
            global c
            c = choice.get()
            if c == '1':
                self.show_frame(CreatePage)
            elif c == '2':
                self.show_frame(ReadPage)
            elif c == '3':
                self.show_frame(UpdatePage)
            elif c == '4':
                self.show_frame(DeletePage)
            elif c == '5':
                self.show_frame(AddCollegePage)
            elif c == '6':
                self.show_frame(ReadDraftPage)
            else:
                self.show_frame(ReadStadiumPage)

        return choice 
     
    def lookup(self,name,season):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_lookup",(name.get(),season.get()))
        result = c2.fetchall()

        if result:
            # exists
            print('exists')
            for row in result:
                tkinter.messagebox.showinfo("Player Information", row) 
                c2.close() 
        else:
            tkinter.messagebox.showinfo("Player Information", 'Player or Season does not exist. Try Again. Make sure both First and Last names are capitalized and the season is in the correct form. You may select from 1997-98 to 2018-19, but it depends on the player.') 
        return

    def draftlookup(self,year):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()

        sqlQuery = "select NBA_3.draftplace(%s);" %year.get();
        c2.execute(sqlQuery);
        result = c2.fetchall()

        inputyear = "NBA_3.draftplace(%s)" %year.get();
        if result[0][inputyear] != None:
            # exists
            for row in result:
                tkinter.messagebox.showinfo("Draft Information", row) 
                c2.close() 
        else:
            tkinter.messagebox.showinfo("Draft Information", 'Draft Year does not exist. Try Again.') 
        return

    
    def stadiumlookup(self,name):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("stadium_lookup",(name.get(),))
        result = c2.fetchall()

        if result:
            # exists
            print('exists')
            for row in result:
                tkinter.messagebox.showinfo("Stadium Information", row) 
                c2.close() 
        else:
            tkinter.messagebox.showinfo("Stadium Information", 'Select Team from List: CHI LAC TOR DAL MIA HOU LAL ATL MIL DEN SEA POR VAN BKN BOS IND SAC MIN PHI ORL SAS PHX DET NO CLE GSW UTA WAS NYK NJN MEM CHA OKC') 

        return

    def create(self,player_name,year_of_draft,college,draft_round,draft_pick_number):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_create",(player_name.get(),year_of_draft.get(),college.get(),draft_round.get(),draft_pick_number.get()))
        
        tkinter.messagebox.showinfo("Alert", "Your new player has been submitted to the database. You may now add statistics.") 
        cnx.commit()
        c2.close() 
        return

    def statcompare(self,player1,season1,player2,season2):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()

        t1 = (player1.get(),season1.get())
        sql="SELECT * FROM NBA_3.playerinstance WHERE player_name = '%s' AND season = '%s';" %t1
        c2.execute(sql)
        result1 = c2.fetchall()
        if result1:
            # exists
            print('exists')
        else:
            tkinter.messagebox.showinfo("Player Information", 'Player One or Season One does not exist. Try Again. Make sure both First and Last names are capitalized and the season is in the correct form. You may select from 1997-98 to 2019-20, but it depends on the player.') 

        t2 = (player2.get(),season2.get())
        sql="SELECT * FROM NBA_3.playerinstance WHERE player_name = '%s' AND season = '%s';" %t2
        c2.execute(sql)
        result2 = c2.fetchall()
        if result2:
            # exists
            print('exists')
        else:
            tkinter.messagebox.showinfo("Player Information", 'Player Two or Season Two does not exist. Try Again. Make sure both First and Last names are capitalized and the season is in the correct form. You may select from 1997-98 to 2019-20, but it depends on the player.') 

        bar_width = 0.35

        x = ['pts','reb','ast','net_rating','oreb_pct','dreb_pct','usg_pct','ts_pct','ast_pct']

        y1 = [float(result1[0][x[i]]) for i in range(len(x))]
        y2 = [float(result2[0][x[i]]) for i in range(len(x))] 

        f = plt.Figure(figsize=(5,5), dpi=75)
        a = f.add_subplot(111)
        plt.setp(a, xticks=range(9), xticklabels=x)
        a.bar(np.array(range(len(x))),y1,bar_width, color='b') 
        a.bar(np.array(range(len(x))) + bar_width,y2,bar_width, color='r') 
        a.legend([result1[0]['player_name']+','+result1[0]['season'],result2[0]['player_name']+','+result2[0]['season']])

        try: 
            self.graph.get_tk_widget().pack_forget()
        except AttributeError: 
            pass              
        self.graph = FigureCanvasTkAgg(f, self)
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        c2.close() 
        return

        
    def addstats(self,player,season,team,age,height ,weight ,gp ,pts ,reb ,ast ,net_rating ,oreb_pct ,dreb_pct ,usg_pct ,ts_pct ,ast_pct):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_addstats",(player.get(),season.get(),team.get(),int(age.get()),int(height.get()) ,int(weight.get()) ,int(gp.get()) ,float(pts.get()) ,float(reb.get()) ,float(ast.get()) ,float(net_rating.get()) ,float(oreb_pct.get()) ,float(dreb_pct.get()),float(usg_pct.get()) ,float(ts_pct.get()) ,float(ast_pct.get())))

        tkinter.messagebox.showinfo("Alert", "Your Player stats have been added to the database.") 
        cnx.commit()
        c2.close()
        return    
    
    def update(self,player_name,year_of_draft,college,draft_round,draft_pick_number):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_update2",(player_name.get(),year_of_draft.get(),college.get(),draft_round.get(),draft_pick_number.get()))
        
        tkinter.messagebox.showinfo("Alert", "Your Player has been updated.") 
        cnx.commit()
        c2.close()

        return
    
    def updatestats(self,player,season,team,age,height ,weight ,gp ,pts ,reb ,ast ,net_rating ,oreb_pct ,dreb_pct ,usg_pct ,ts_pct ,ast_pct):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_update",(player.get(),season.get(),team.get(),int(age.get()),int(height.get()) ,int(weight.get()) ,int(gp.get()) ,float(pts.get()) ,float(reb.get()) ,float(ast.get()) ,float(net_rating.get()) ,float(oreb_pct.get()) ,float(dreb_pct.get()),float(usg_pct.get()) ,float(ts_pct.get()) ,float(ast_pct.get())))

        tkinter.messagebox.showinfo("Alert", "Your Player has been updated.") 
        cnx.commit()
        c2.close()
        return  
    
    def delete(self,player_name):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("player_delete",(player_name.get(),))

        tkinter.messagebox.showinfo("Alert", "Your Player has been deleted.") 
        cnx.commit()
        c2.close()
        return
    
    def addcollege(self,name,country):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        c2.callproc("add_college",(name.get(),country.get()))

        tkinter.messagebox.showinfo("Alert", "Your college has been added to the database.") 
        cnx.commit()
        c2.close()
        return

    def deletecollege(self,name,country):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()
        #sql="SELECT * FROM NBA_3.college WHERE college = '%s';" %name.get()
        #c2.execute(sql)
        #result_test = c2.fetchall()
        #print(result_test)

        c2.callproc("delete_college",(name.get(),country.get()))

        result = c2.fetchall()
        if result:
            print('exists')
            for row in result:
                tkinter.messagebox.showinfo("Alert", "Your college has been deleted from the database.") 
                cnx.commit()
                c2.close() 
        else:
            tkinter.messagebox.showinfo("College Information", 'College does not exist') 

        c2.close()
        return
    
    def collegeanalytics(self):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()

        sql="SELECT college,count(*) as c FROM NBA_3.player GROUP BY college ORDER BY c desc LIMIT 10;"
        c2.execute(sql)
        myresult1 = c2.fetchall()

        bar_width = 0.35

        y1 = [myresult1[i]['c'] for i in range(10)]
        x = [myresult1[i]['college'] for i in range(10)]
        
        f = plt.Figure(figsize=(5,5), dpi=75)
        a = f.add_subplot(111)
        plt.setp(a, xticks=range(10), xticklabels=x)
        a.bar(x,y1,bar_width, color='b')
        #a.ylabel("Number of Players per College")
        try: 
            self.graph.get_tk_widget().pack_forget()
        except AttributeError: 
            pass              
        self.graph = FigureCanvasTkAgg(f, self)
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        c2.close() 
        return
    
    def draftanalytics(self):
        cnx = pymysql.connect(host = 'localhost',user = u ,password  = p,db = 'NBA_3',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        c2 = cnx.cursor()

        sql="SELECT city, count(*) as c FROM NBA_3.draft GROUP BY city ORDER BY c desc;"
        c2.execute(sql)
        myresult1 = c2.fetchall()

        bar_width = 0.35

        y1 = [myresult1[i]['c'] for i in range(len(myresult1))]
        x = [myresult1[i]['city'] for i in range(len(myresult1))]
        
        f = plt.Figure(figsize=(5,5), dpi=75)
        a = f.add_subplot(111)
        plt.setp(a, xticks=range(len(myresult1)), xticklabels=x)
        a.bar(x,y1,bar_width, color='b')
        #a.ylabel("Number of Players per College")
        try: 
            self.graph.get_tk_widget().pack_forget()
        except AttributeError: 
            pass               
        self.graph = FigureCanvasTkAgg(f, self)
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        c2.close() 
        return
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')
        
        label = tk.Label(self, text='Login to the NBA Database', font=LARGEST_FONT)
        label.pack(pady=10, padx=10)
        
        #username label and text entry box
        usernameLabel = tk.Label(self, text="User Name")
        usernameLabel.pack(pady=10, padx=10)

        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username)
        usernameEntry.pack(pady=10, padx=10)

        #password label and password entry box
        passwordLabel = tk.Label(self,text="Password") 
        passwordLabel.pack(pady=10, padx=10)

        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=password, show='*')
        passwordEntry.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text='Login', 
                            command=lambda : controller.validateLogin(username, password, PageOne))
        button1.pack() 
        
        
class PageOne(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')
         
        label = tk.Label(self, text='Main Menu', font=LARGEST_FONT)
        label.pack(pady=10, padx=10)

        choiceLabel = tk.Label(self, text="What would you like to do? Type 1,2,3,4,5,6,7 for: \n1. Create a new player. \n2. Lookup/compare a player's stats. \n3. Update a Player. \n4. Delete a player.\n5. Add/Delete a College\n6. Lookup Draft Information\n7. Lookup Team Stadium")
        choiceLabel.pack(pady=10, padx=10)

        readmeLabel = tk.Label(self, text="")
        #readmeLabel.pack(pady=10, padx=10)

        choice = tk.StringVar()
        choiceEntry = tk.Entry(self, textvariable=choice)
        choiceEntry.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text='Enter',
                            command=lambda : controller.get_task(choice))
        button1.pack()
        
        tk.Button(self, text="Log Out", command=parent.destroy).pack() 
  
    
class CreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Create a New Player', font=LARGEST_FONT)
        label.pack(pady=10, padx=10)

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.pack(pady=10, padx=10)

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.pack(pady=10, padx=10)

        yearLabel = tk.Label(self, text="Year of Draft")
        yearLabel.pack(pady=10, padx=10)
        
        label = tk.Label(self, text='Must be between 1963-2019')
        label.pack(pady=10, padx=10)

        year = tk.StringVar()
        yearEntry = tk.Entry(self, textvariable=year)
        yearEntry.pack(pady=10, padx=10)
        
        collegeLabel = tk.Label(self, text="College")
        collegeLabel.pack(pady=10, padx=10)

        college = tk.StringVar()
        collegeEntry = tk.Entry(self, textvariable=college)
        collegeEntry.pack(pady=10, padx=10)
        
        roundLabel = tk.Label(self, text="Draft Round")
        roundLabel.pack(pady=10, padx=10)

        round_ = tk.StringVar()
        round_Entry = tk.Entry(self, textvariable=round_)
        round_Entry.pack(pady=10, padx=10)
        
        pickLabel = tk.Label(self, text="Draft Pick Number")
        pickLabel.pack(pady=10, padx=10)

        pick = tk.StringVar()
        pickEntry = tk.Entry(self, textvariable=pick)
        pickEntry.pack(pady=10, padx=10)
        
        button2 = tk.Button(self, text='Submit',
                            command=lambda : controller.create(name,year,college,round_,pick))  
        
        button2.pack()
        
        button3 = tk.Button(self, text='Add Stats',
                            command=lambda : controller.show_frame(CreateStatsPage))  
        
        button3.pack()

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.pack()

class CreateStatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Add Stats to a Player', font=LARGEST_FONT)
        label.grid(row = 0,column = 1)

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.grid(row = 1,column = 0)

        label = tk.Label(self, text='Player must exist in DB.')
        label.grid(row = 1,column = 2)

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.grid(row = 1,column = 1)

        seasonLabel = tk.Label(self, text="Season (i.e. 1998-99)")
        seasonLabel.grid(row = 2,column = 0)

        season = tk.StringVar()
        seasonEntry = tk.Entry(self, textvariable=season)
        seasonEntry.grid(row = 2,column = 1)
        
        button = tk.Button(self, text='Check valid', command = lambda : tkinter.messagebox.showinfo("Alert", 'Season must be between 1996-97 and 2019-20.'), bg="gray")
        button.grid(row = 2,column = 2)
        
        teamLabel = tk.Label(self, text="Team Abbreviation")
        teamLabel.grid(row = 3,column = 0)

        team = tk.StringVar()
        teamEntry = tk.Entry(self, textvariable=team)
        teamEntry.grid(row = 3,column = 1)
        
        button = tk.Button(self, text='Check valid', command = lambda : tkinter.messagebox.showinfo("Alert", 'Select Team from List: CHI LAC TOR DAL MIA HOU LAL ATL MIL DEN SEA POR VAN BKN BOS IND SAC MIN PHI ORL SAS PHX DET NO CLE GSW UTA WAS NYK NJN MEM CHA OKC'), bg="gray")
        button.grid(row = 3,column = 2)
        
        ageLabel = tk.Label(self, text="Age")
        ageLabel.grid(row = 4,column = 0)

        age = tk.StringVar()
        ageEntry = tk.Entry(self, textvariable=age)
        ageEntry.grid(row = 4,column = 1) # center alignment
    
        heightLabel = tk.Label(self, text="Height")
        heightLabel.grid(row = 5,column = 0) # center alignment

        height = tk.StringVar()
        heightEntry = tk.Entry(self, textvariable=height)
        heightEntry.grid(row = 5,column = 1) # center alignment

        weightLabel = tk.Label(self, text="Weight")
        weightLabel.grid(row = 6,column = 0) # center alignment

        weight = tk.StringVar()
        weightEntry = tk.Entry(self, textvariable=weight)
        weightEntry.grid(row = 6,column = 1) # center alignment

        gpLabel = tk.Label(self, text="Games Played")
        gpLabel.grid(row = 7,column = 0) # center alignment

        gp = tk.StringVar()
        gpEntry = tk.Entry(self, textvariable=gp)
        gpEntry.grid(row = 7,column = 1) # center alignment

        ptsLabel = tk.Label(self, text="Points Per Game")
        ptsLabel.grid(row = 8,column = 0) # center alignment

        pts = tk.StringVar()
        ptsEntry = tk.Entry(self, textvariable=pts)
        ptsEntry.grid(row = 8,column = 1) # center alignment

        rebLabel = tk.Label(self, text="Rebounds Per Game")
        rebLabel.grid(row = 9,column = 0) # center alignment

        reb = tk.StringVar()
        rebEntry = tk.Entry(self, textvariable=reb)
        rebEntry.grid(row = 9,column = 1) # center alignment
        
        astLabel = tk.Label(self, text="Assists Per Game")
        astLabel.grid(row = 10,column = 0) # center alignment

        ast = tk.StringVar()
        astEntry = tk.Entry(self, textvariable=ast)
        astEntry.grid(row = 10,column = 1) # center alignment

        netLabel = tk.Label(self, text="Net Rating")
        netLabel.grid(row = 11,column = 0) # center alignment

        net = tk.StringVar()
        netEntry = tk.Entry(self, textvariable=net)
        netEntry.grid(row = 11,column = 1) # center alignment

        orebLabel = tk.Label(self, text="Offensive Rebound %")
        orebLabel.grid(row = 12,column = 0) # center alignment

        oreb = tk.StringVar()
        orebEntry = tk.Entry(self, textvariable=oreb)
        orebEntry.grid(row = 12,column = 1) # center alignment

        drebLabel = tk.Label(self, text="Defensive Rebound %")
        drebLabel.grid(row = 13,column = 0) # center alignment

        dreb = tk.StringVar()
        drebEntry = tk.Entry(self, textvariable=dreb)
        drebEntry.grid(row = 13,column = 1) # center alignment

        usgLabel = tk.Label(self, text="Usage %")
        usgLabel.grid(row = 14,column = 0) # center alignment

        usg = tk.StringVar()
        usgEntry = tk.Entry(self, textvariable=usg)
        usgEntry.grid(row = 14,column = 1) # center alignment

        tsLabel = tk.Label(self, text="Turnover %")
        tsLabel.grid(row = 15,column = 0) # center alignment

        ts = tk.StringVar()
        tsEntry = tk.Entry(self, textvariable=ts)
        tsEntry.grid(row = 15,column = 1) # center alignment

        astpLabel = tk.Label(self, text="Assist %")
        astpLabel.grid(row = 16,column = 0) # center alignment

        astp = tk.StringVar()
        astpEntry = tk.Entry(self, textvariable=astp)
        astpEntry.grid(row = 16,column = 1) # center alignment

        button3 = tk.Button(self, text='Add', # likewise StartPage
                            command=lambda : controller.addstats(name,season,team,age,height ,weight ,gp ,pts ,reb ,ast ,net ,oreb ,dreb ,usg ,ts ,astp))  
        
        button3.grid(row = 17,column = 1) # pack it in       

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.grid(row = 18,column = 1) # pack it in

class ReadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Read a Player Instance', font=LARGEST_FONT)
        label.pack()

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.pack()

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.pack()
        
        seasonLabel = tk.Label(self, text="Season (i.e. 1998-99)")
        seasonLabel.pack()

        season = tk.StringVar()
        seasonEntry = tk.Entry(self, textvariable=season)
        seasonEntry.pack()
        
        button3 = tk.Button(self, text='Enter',
                            command=lambda : controller.lookup(name,season))  
        
        button3.pack()

        nameLabel2 = tk.Label(self, text="Addition Player Name")
        nameLabel2.pack()

        name2 = tk.StringVar()
        nameEntry2 = tk.Entry(self, textvariable=name2)
        nameEntry2.pack()
        
        seasonLabel2 = tk.Label(self, text="Season (i.e. 1998-99)")
        seasonLabel2.pack()

        season2 = tk.StringVar()
        seasonEntry2 = tk.Entry(self, textvariable=season2)
        seasonEntry2.pack()

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.pack()
        
        plot_button = tk.Button(self,  
                     command = lambda : controller.statcompare(name,season,name2,season2), 
                     height = 2,  
                     width = 10, 
                     text = "Compare Stats") 
  
        plot_button.pack()


class ReadStadiumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text="Lookup a Team's Stadium", font=LARGEST_FONT)
        label.pack(pady=10, padx=10)

        nameLabel = tk.Label(self, text="Team Abbreviation")
        nameLabel.pack(pady=10, padx=10) # center alignment

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.pack(pady=10, padx=10) # center alignment
        
        button3 = tk.Button(self, text='Enter', # likewise StartPage
                            command=lambda : controller.stadiumlookup(name))  
        
        button3.pack() # pack it in

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.pack() # pack it in

class UpdatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Update a Player', font=LARGEST_FONT)
        label.pack(pady=10, padx=10)

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.pack(pady=10, padx=10) # center alignment
        label = tk.Label(self, text='Player must exist in DB')
        label.pack(pady=10, padx=10)
        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.pack(pady=10, padx=10) # center alignment

        yearLabel = tk.Label(self, text="Year of Draft")
        yearLabel.pack(pady=10, padx=10) # center alignment
        
        label = tk.Label(self, text='Must be between 1963-2019')
        label.pack(pady=10, padx=10)
        
        year = tk.StringVar()
        yearEntry = tk.Entry(self, textvariable=year)
        yearEntry.pack(pady=10, padx=10) # center alignment
        
        collegeLabel = tk.Label(self, text="College")
        collegeLabel.pack(pady=10, padx=10) # center alignment
        
        label = tk.Label(self, text='College must exist in DB')
        label.pack(pady=10, padx=10)

        college = tk.StringVar()
        collegeEntry = tk.Entry(self, textvariable=college)
        collegeEntry.pack(pady=10, padx=10) # center alignment
        
        roundLabel = tk.Label(self, text="Draft Round")
        roundLabel.pack(pady=10, padx=10) # center alignment

        round_ = tk.StringVar()
        round_Entry = tk.Entry(self, textvariable=round_)
        round_Entry.pack(pady=10, padx=10) # center alignment
        
        pickLabel = tk.Label(self, text="Draft Pick Number")
        pickLabel.pack(pady=10, padx=10) # center alignment

        pick = tk.StringVar()
        pickEntry = tk.Entry(self, textvariable=pick)
        pickEntry.pack(pady=10, padx=10) # center alignment
        
        button2 = tk.Button(self, text='Update',
                            command=lambda : controller.update(name,year,college,round_,pick))  
        
        button2.pack() # pack it in
        
        button3 = tk.Button(self, text='Update Stats',
                            command=lambda : controller.show_frame(UpdateStatsPage))  
        
        button3.pack() # pack it in

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.pack() # pack it in
        
class UpdateStatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text="Update a Player's Stats (Fill in all fields)", font=LARGEST_FONT)
        label.grid(row = 0,column = 1)

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.grid(row = 1,column = 0) # center alignment

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.grid(row = 1,column = 1) # center alignment

        label = tk.Label(self, text='Player must exist in DB.')
        label.grid(row = 1,column = 2)

        seasonLabel = tk.Label(self, text="Season (i.e. 1998-99)")
        seasonLabel.grid(row = 2,column = 0)

        season = tk.StringVar()
        seasonEntry = tk.Entry(self, textvariable=season)
        seasonEntry.grid(row = 2,column = 1)
        
        button = tk.Button(self, text='Check valid', command = lambda : tkinter.messagebox.showinfo("Alert", 'Season must be between 1996-97 and 2019-20.'),bg="gray")
        button.grid(row = 2,column = 2)
        
        teamLabel = tk.Label(self, text="Team Abbreviation")
        teamLabel.grid(row = 3,column = 0)

        team = tk.StringVar()
        teamEntry = tk.Entry(self, textvariable=team)
        teamEntry.grid(row = 3,column = 1)
        
        button = tk.Button(self, text='Check valid', command = lambda : tkinter.messagebox.showinfo("Alert", 'Select Team from List: CHI LAC TOR DAL MIA HOU LAL ATL MIL DEN SEA POR VAN BKN BOS IND SAC MIN PHI ORL SAS PHX DET NO CLE GSW UTA WAS NYK NJN MEM CHA OKC'),bg="gray")
        button.grid(row = 3,column = 2)


        ageLabel = tk.Label(self, text="Age")
        ageLabel.grid(row = 4,column = 0) # center alignment

        age = tk.StringVar()
        ageEntry = tk.Entry(self, textvariable=age)
        ageEntry.grid(row = 4,column = 1) # center alignment
    
        heightLabel = tk.Label(self, text="Height")
        heightLabel.grid(row = 5,column = 0) # center alignment

        height = tk.StringVar()
        heightEntry = tk.Entry(self, textvariable=height)
        heightEntry.grid(row = 5,column = 1) # center alignment

        weightLabel = tk.Label(self, text="Weight")
        weightLabel.grid(row = 6,column = 0) # center alignment

        weight = tk.StringVar()
        weightEntry = tk.Entry(self, textvariable=weight)
        weightEntry.grid(row = 6,column = 1) # center alignment

        gpLabel = tk.Label(self, text="Games Played")
        gpLabel.grid(row = 7,column = 0) # center alignment

        gp = tk.StringVar()
        gpEntry = tk.Entry(self, textvariable=gp)
        gpEntry.grid(row = 7,column = 1) # center alignment

        ptsLabel = tk.Label(self, text="Points Per Game")
        ptsLabel.grid(row = 8,column = 0) # center alignment

        pts = tk.StringVar()
        ptsEntry = tk.Entry(self, textvariable=pts)
        ptsEntry.grid(row = 8,column = 1) # center alignment

        rebLabel = tk.Label(self, text="Rebounds Per Game")
        rebLabel.grid(row = 9,column = 0) # center alignment

        reb = tk.StringVar()
        rebEntry = tk.Entry(self, textvariable=reb)
        rebEntry.grid(row = 9,column = 1) # center alignment
        
        astLabel = tk.Label(self, text="Assists Per Game")
        astLabel.grid(row = 10,column = 0) # center alignment

        ast = tk.StringVar()
        astEntry = tk.Entry(self, textvariable=ast)
        astEntry.grid(row = 10,column = 1) # center alignment

        netLabel = tk.Label(self, text="Net Rating")
        netLabel.grid(row = 11,column = 0) # center alignment

        net = tk.StringVar()
        netEntry = tk.Entry(self, textvariable=net)
        netEntry.grid(row = 11,column = 1) # center alignment

        orebLabel = tk.Label(self, text="Offensive Rebound %")
        orebLabel.grid(row = 12,column = 0) # center alignment

        oreb = tk.StringVar()
        orebEntry = tk.Entry(self, textvariable=oreb)
        orebEntry.grid(row = 12,column = 1) # center alignment

        drebLabel = tk.Label(self, text="Defensive Rebound %")
        drebLabel.grid(row = 13,column = 0) # center alignment

        dreb = tk.StringVar()
        drebEntry = tk.Entry(self, textvariable=dreb)
        drebEntry.grid(row = 13,column = 1) # center alignment

        usgLabel = tk.Label(self, text="Usage %")
        usgLabel.grid(row = 14,column = 0) # center alignment

        usg = tk.StringVar()
        usgEntry = tk.Entry(self, textvariable=usg)
        usgEntry.grid(row = 14,column = 1) # center alignment

        tsLabel = tk.Label(self, text="Turnover %")
        tsLabel.grid(row = 15,column = 0) # center alignment

        ts = tk.StringVar()
        tsEntry = tk.Entry(self, textvariable=ts)
        tsEntry.grid(row = 15,column = 1) # center alignment

        astpLabel = tk.Label(self, text="Assist %")
        astpLabel.grid(row = 16,column = 0) # center alignment

        astp = tk.StringVar()
        astpEntry = tk.Entry(self, textvariable=astp)
        astpEntry.grid(row = 16,column = 1) # center alignment

        button3 = tk.Button(self, text='Update', # likewise StartPage
                            command=lambda : controller.updatestats(name,season,team,age,height ,weight ,gp ,pts ,reb ,ast ,net ,oreb ,dreb ,usg ,ts ,astp))  
        
        button3.grid(row = 17,column = 1) # pack it in       

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.grid(row = 18,column = 1) # pack it in

class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Delete a Player', font=LARGEST_FONT)
        label.grid(row = 0,column = 5)

        nameLabel = tk.Label(self, text="Player Name")
        nameLabel.grid(row = 1,column = 0) # center alignment

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.grid(row = 1,column = 1) # center alignment
        
        button3 = tk.Button(self, text='Delete', # likewise StartPage
                            command=lambda : controller.delete(name))  
        
        button3.grid(row = 3,column = 5) # pack it in

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.grid(row = 4,column = 5) # pack it in

class AddCollegePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Add a College to the Database', font=LARGEST_FONT)
        label.grid(row = 0,column = 5)

        nameLabel = tk.Label(self, text="College Name")
        nameLabel.grid(row = 1,column = 0) # center alignment

        name = tk.StringVar()
        nameEntry = tk.Entry(self, textvariable=name)
        nameEntry.grid(row = 1,column = 1) # center alignment

        countryLabel = tk.Label(self, text="Country")
        countryLabel.grid(row = 2,column = 0) # center alignment

        country = tk.StringVar()
        countryEntry = tk.Entry(self, textvariable=country)
        countryEntry.grid(row = 2,column = 1) # center alignment
        
        button3 = tk.Button(self, text='Add', # likewise StartPage
                            command=lambda : controller.addcollege(name,country))  
        
        button3.grid(row = 3,column = 5) # pack it in
        
        button5 = tk.Button(self, text='Delete', # likewise StartPage
                            command=lambda : controller.deletecollege(name,country))  
        
        button5.grid(row = 4,column = 5) # pack it in
        
        button4 = tk.Button(self, text='College Analytics',
                            command=lambda : controller.collegeanalytics())  
        
        button4.grid(row = 6,column = 5) # pack it in

        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.grid(row = 7,column = 5) # pack it in

class ReadDraftPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#49A')

        label = tk.Label(self, text='Lookup a Draft Location', font=LARGEST_FONT)
        label.pack()

        yearLabel = tk.Label(self, text="Draft Year")
        yearLabel.pack()

        year = tk.StringVar()
        yearEntry = tk.Entry(self, textvariable=year)
        yearEntry.pack()
        
        
        button3 = tk.Button(self, text='Enter', # likewise StartPage
                            command=lambda : controller.draftlookup(year))  
        
        button3.pack()


        button4 = tk.Button(self, text='Home',
                            command=lambda : controller.show_frame(PageOne))  
        
        button4.pack()
        
        button5 = tk.Button(self, text='Draft Stats',
                            command=lambda : controller.draftanalytics())
        
        button5.pack()
        
        

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
