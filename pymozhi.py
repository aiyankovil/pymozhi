import patterns
import re
from Tkinter import *

def transword(wd):
    dict_trans=patterns.getDictTrans()
    pattern=patterns.getPat()
    result=[]
    while len(wd)>0:
        M=re.match(pattern,wd)
        if M.group(0) in dict_trans.keys():
            result.append(dict_trans[M.group(0)])
            wd=wd[M.end():]
        else:
            result.append(wd[0])
            wd=wd[1:]
    return result
            
def str_result(r):
    w=''
    for l in r:
        w+=l
    return w

class MyApp:
    def __init__(self, parent):        
        self.myParent = parent 
        self.myParent.geometry("640x500")
        
        ### Our topmost frame is called myContainer
        self.myContainer = Frame(parent) ###
        self.myContainer.pack(expand=YES, fill=BOTH)

        ### We will use HORIZONTAL (left/right) orientation inside myContainer.
        ### Inside myContainer1, we create top_frame and bottom_frame.

        # top frame
        self.top_frame = Frame(self.myContainer,height=200)
        self.top_frame.pack(side=TOP, fill=X)  ###

        # bottom frame
        self.bottom_frame = Frame(self.myContainer,
            borderwidth=5,  relief=RIDGE,
            height=200, 
            bg="cyan",
            )
        self.bottom_frame.pack(side=TOP, fill=X)        
                
        # inside top_frame we create a textbox         
        self.eng_text = Text(self.top_frame)
        self.eng_text.pack()
        self.eng_text.bind("<Key>", self.translate) ### (2)        
       
        # inside bottom_frame we create a textbox         
        self.mal_text = Text(self.bottom_frame)
        self.mal_text.pack()
    
    def translate(self,event):
        if str(event.keysym)=='space':
            mang = str(self.eng_text.get(0.0, END))
            str_res=''
            for w in mang.split(' '):
                result=transword(w)
                str_res+=str_result(result)+' '
            
            self.mal_text.delete(0.0, END)
            self.mal_text.insert(0.0, str_res)
#just a git bash test
root = Tk()
myapp = MyApp(root)
root.mainloop()
