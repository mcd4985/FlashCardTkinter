
#!/usr/bin/env python
from decorator import decorator

from tkinter import *
import pandas as pd
import sys


@decorator
def on_start(func,*args, **kwargs):
    if kwargs !={}:
        try:
            if kwargs['Start']:
                if 'Verbose' in kwargs['Settings']:
                    if kwargs['Settings']['Verbose']:
                        print(func)
                        pass
                response= func(*args,**kwargs)
                return response
            else:
                kwargs['Start'] = False
                print(func,"DID NOT START")
                return(kwargs)
        except Exception as e:
            print('NODE ERROR OCCURED TRYING TO START NODE FUNCTION:')
            print('===========================================')
            print(func,e)
            print('===========================================')
            print('LAST STATE SET TO:')
            print('===========================================')
            print('ekwargs')
            print('===========================================')
            print('LAST NODE FUNCTION SET TO:')
            print('===========================================')
            print('efunc')
            print('===========================================')
            global ekwargs
            global efunc
            ekwargs = kwargs
            efunc = func
            print('HALTING')
            raise
    else:
        print('Empty kwargs')
        return ()



def start():
    return {'Start':True,'Settings':{'Verbose':True},'Status':{},'Data':[],'Threads':[]}

 
@on_start
def excel2Pandas1(*args,**kwargs):
    
    df = pd.read_excel('IntroNeuroFlashcards.xlsx')
    
    kwargs['Data'] = df
    
    return kwargs
      
 
@on_start
def showFlashCards2(*args,**kwargs):
    
    global thisCard, returnCardBtn, removeCardBtn
    
    def flipCard():
        
        global thisCard, removeCardBtn, returnCardBtn
        
        lbl.configure(text=thisCard.Back.values[0], fg='red')
        flipBtn.grid_forget()
        returnCardBtn = Button(window, text="Return Card to Deck", command=returnCard)
        returnCardBtn.grid(column=0, row=1)
        removeCardBtn = Button(window, text="Remove Card from Deck", command=removeCard)
        removeCardBtn.grid(column=1, row=1)
        
    def returnCard():
        
        global thisCard
        
        thisCard = df.sample()  #selects a random sample from the dataframe
        lbl.configure(text=thisCard.Front.values[0], fg='black')
        returnCardBtn.grid_forget()
        removeCardBtn.grid_forget()
        flipBtn.grid(column=0, row=1, columnspan=2)
        
    def removeCard():
        global thisCard, returnCardBtn, removeCardBtn
        
        if df.any(axis=None):
            
            df.drop(thisCard.index, inplace=True)
            
            if not df.empty:
                
                thisCard = df.sample()  #selects a random sample from the dataframe
                lbl.configure(text=thisCard.Front.values[0], fg='black')
                returnCardBtn.grid_forget()
                removeCardBtn.grid_forget()
                flipBtn.grid(column=0, row=1, columnspan=2)
            
            else:
                lbl.configure(text="Complete!", fg='blue')
            
            
    df = kwargs['Data']
    
    thisCard = df.sample()  #selects a random sample from the dataframe
    window = Tk()
    window.geometry('700x400')
    lbl = Label(window, text=thisCard.Front.values[0], font=20, width=60, pady=50, wraplength=450, justify=CENTER)
    lbl.grid(column=0, row=0, columnspan=2)
    flipBtn = Button(window, text="Flip Card", command=flipCard)
    flipBtn.grid(column=0, row=1, columnspan=2)
    window.mainloop()
    
    
    return kwargs
      
 
@on_start
def stop(*args,**kwargs):
    print('exiting')
    sys.exit()
 
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=stop(**showFlashCards2(**excel2Pandas1(**kwargs)))
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        self.status="pending"
    def run(self,expname):
        self.response=stop(**showFlashCards2(**excel2Pandas1(**start())))
        self.status="completed"
        return(self.status)

if __name__ == '__main__':
    process = liveprocess()
    process.run('Local')
    