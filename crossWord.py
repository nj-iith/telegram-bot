
import pickle
import sys
import requests
import re
from bs4 import BeautifulSoup
import random
def good_sen(sen):
    if sen.split()[0]=="This" :
        return False
    goodboys="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    nice=True
    for letter in sen:
        no=0
        if nice==False:
            break
        for boy in goodboys:
            if letter==boy:
                no+=1
                break
        if no==0:
            nice=False
            break
    return nice
def wikirip():
    ab="abcdefghijklmnopqrstuvwxyz"
    Search=""
    n=random.randrange(5,20)
    for i in range(n):
        Search+=random.choice(ab)
    try:
        addr="https://en.wikipedia.org/wiki/Special:AllPages/"+Search
    except:
        print("Network problem")
        sys.exit()
    page=requests.get(addr)
    list_page = BeautifulSoup(page.text, 'html.parser')
    aaa=list_page.find("li",class_="allpagesredirect")
    aaaa=aaa.find('a')
    wiki_page_addr="https://en.wikipedia.org"+aaaa["href"]
    # wiki_page_addr="https://en.wikipedia.org/wiki/Usvyatsky_District"
    page2=BeautifulSoup(requests.get(wiki_page_addr).text, 'html.parser')
    para=page2.find("p")
    sen= para.get_text().split(".")[0]
    
    try:
        done=False
        while not done:
            for i in range(len(sen)):
                if sen[i]=="(":
                    break
            opened=0
            for j in range(len(sen)):
                if sen[j]=="(":
                    opened+=1
                elif sen[j]==")":
                    if opened<2 :
                        break
                    else:
                        opened-=1
            if i==j :
                done=True
                break
            sen=sen[0:i]+sen[j+1:]
        done=False
        while not done:
            for i in range(len(sen)):
                if sen[i]=="[":
                    break
            opened=0
            for j in range(len(sen)):
                if sen[j]=="[":
                    opened+=1
                elif sen[j]=="]":
                    if opened<2 :
                        break
                    else:
                        opened-=1
            if i==j :
                done=True
                break
            sen=sen[0:i]+sen[j+1:]
        spl=sen.split()
        if len(spl)<3 or not good_sen(spl[0]) or not good_sen(spl[1]):
            return wikirip()
        elif spl[1]=="is" or spl[2]=="is":
            ans=""
            question=""
            passed=False
            for i in spl:
                if i=="is":
                    passed=True
                elif passed:
                    question+=i+" "
                else:
                    ans+=i
            ans=ans
            ans=ans.upper()
            question=question[0].upper()+question[1:]
            return question,ans
        elif spl[1]=="was" or spl[2]=="was":
            ans=""
            question=""
            passed=False
            for i in spl:
                if i=="was":
                    passed=True
                elif passed:
                    question+=i+" "
                else:
                    ans+=i
            ans=ans.upper()
            question=question[0].upper()+question[1:]
            return question,ans
        else:
            return wikirip()
    except:
        wikirip()




class Clue:
    def __init__(self,text,number,direction):
        self.text=text
        self.number=number
        self.direction=direction
class cell:
    def __init__(self):
        self.char='#'
        self.num=None
class CrossWord:
    def __init__(self,size):
        self.size=size
        self.grid=[[cell() for i in range(size)] for j in range(size)]
        self.clues=[]
        self.num=0
    def Print(self):
        for y in self.grid:
            for x in y:
                if x.char==None:
                    print("#",end=" ")
                else:
                    print(x.char,end=" ")
            print("")
    def Print_nice(self):
        for y in self.grid:
            for x in y:
                if x.char==None or x.char=="|" or x.char=="_" or x.char=="/" or x.char=="#":
                    print(" ",end=" ")
                else:
                    print(x.char,end=" ")
            print("")
    def Print_num(self):
        for y in self.grid:
            for x in y:
                if x.num==None:
                    print(" ",end=" ")
                else:
                    print(x.num,end=" ")
            print("")
    def Print_clues(self):
        for c in self.clues:
            print(c.number,". ",c.text," (", "Across" if c.direction=="_" else "Downwards",").")
    def check(self,text,dir):
        if (len(text)>self.size):
            return False,(None,None)
        if dir=='_':
            for y in range(0,self.size):
                for x in range(0,self.size-len(text)):
                    cross=False
                    placable=True
                    i=0
                    for l in text:
                        if(self.grid[y][x+i].char==l):
                            cross=True
                        if not(self.grid[y][x+i].char==l or self.grid[y][x+i].char=="#" or self.grid[y][x+i].char=="_"):
                            placable=False
                        i+=1
                    if (self.grid[y][x+i].char not in ['#','|','/','_']):
                        placable=False
                    if placable and cross:
                        return True,(x,y)
        else:
            for y in range(0,self.size-len(text)):
                for x in range(0,self.size):
                    cross=False
                    placable=True
                    i=0
                    for l in text:
                        if(self.grid[y+i][x].char==l):
                            cross=True
                        if not(self.grid[y+i][x].char==l or self.grid[y+i][x].char=="#" or self.grid[y+i][x].char=="|"):
                            placable=False
                        i+=1
                    if placable and cross:
                        return True,(x,y)
        return False,(None,None)

    def fill(self,text,pos,dir):
        
        x,y=pos
        if self.grid[y][x].num==None :
            self.num+=1
            self.grid[y][x].num=self.num

        
        if dir=='_' :
            if (x>0):
                if self.grid[y][x-1].char=="#" or self.grid[y][x-1].char=="|" or self.grid[y][x-1].char=="_":
                    self.grid[y][x-1].char="/"
        else:
            if (y>0):
                if self.grid[y-1][x].char=="#" or self.grid[y-1][x].char=="|" or self.grid[y-1][x].char=="_":
                    self.grid[y-1][x].char=="/"
        for c in text:
            self.grid[y][x].char=c
            if dir=='_' :
                if(x+1<self.size):
                    if self.grid[y][x+1].char=="#" or self.grid[y][x+1].char=="|" or self.grid[y][x+1].char=="_":
                        self.grid[y][x+1].char="/"
                if(y>0):
                    if self.grid[y-1][x].char=="#":
                        self.grid[y-1][x].char="|"
                    elif self.grid[y-1][x].char=="_":
                        self.grid[y-1][x].char="/"
                if(y<self.size-1):
                    if self.grid[y+1][x].char=="#":
                        self.grid[y+1][x].char="|"
                    elif self.grid[y+1][x].char=="_":
                        self.grid[y+1][x].char="/"

                x+=1
                
            else:
                if(y+1<self.size):
                    if self.grid[y+1][x].char=="#" or self.grid[y+1][x].char=="|" or self.grid[y+1][x].char=="_":
                        self.grid[y+1][x].char="/"
                if(x>0):
                    if self.grid[y][x-1].char=="#":
                        self.grid[y][x-1].char="_"
                    elif self.grid[y][x-1].char=="|":
                        self.grid[y][x-1].char="/"

                if(x<self.size-1):
                    if self.grid[y][x+1].char=="#":
                        self.grid[y][x+1].char="_"
                    elif self.grid[y][x+1].char=="|":
                        self.grid[y][x+1].char="/"
                y+=1
        x,y=pos
        return self.grid[y][x].num

    def generate(self):
        a=(self.size+1)*"X"
        while len(a)>self.size :
            q,a=wikirip()
        self.fill(a,(0,0),'_')
        self.clues.append(Clue(q,1,"_"))
        print("?:",q,"\n\n\n")
        print("A:",a,"\n\n\n")
        self.Print()
        dir="_"
        rep=0
        Try=0
        while rep<(self.size*2)//3 :
            if dir=="_":
                dir="|"
            else:
                dir="_"
            ok=False
            Try=1
            while not ok:
                got=False
                while not got:
                    try:
                        q,a=wikirip()
                        got=True
                    except:
                        pass
                print("try",Try,":",a)
                print("\nxxxxxxxx\n",self.check(a,dir),"\nxxxxxxxxxxxxxx\n")
                ok,pos=self.check(a,dir)
                if ok :
                    num=self.fill(a,pos,dir)
                    self.clues.append(Clue(q,num,dir))
                    print("?:",q,"\n\n\n")
                    print("A:",a,"\n\n\n")
                    self.Print()
                Try+=1
                if(Try>self.size):
                    break
            rep+=1
        print("\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        self.Print_clues()
        print("\n\n______________________________________________\n\n")
        self.Print_nice()
        print("\n\n______________________________________________\n\n")
        self.Print_num()

        
if __name__=='__main__':
    c=CrossWord(15)
    c.generate()
    with open("file.bin","wb") as file:
        pickle.dump(c,file)