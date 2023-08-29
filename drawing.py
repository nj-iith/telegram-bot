import pickle
from  crossWord import*
from PIL import Image, ImageDraw ,ImageFont


def Draw(c):
    img = Image.new('RGB', (1920,1080), (255,255,255))
    font = ImageFont.truetype("font2.ttf", 15)
    font2=ImageFont.truetype("font2.ttf", 20)
    font3=ImageFont.truetype("font3.ttf", 25)
    font4=ImageFont.truetype("font2.ttf", 100)
    Draw1 = ImageDraw.Draw(img) 

    for y in range(c.size):
        for x in range(c.size):
            if (c.grid[y][x].char!="#" and c.grid[y][x].char!="|" and c.grid[y][x].char!="/" and c.grid[y][x].char!="_"):
                shape = [(125+x*50, 205+y*50), (175+x*50, 255+y*50)] 
                Draw1.rectangle(shape, fill =(230,230,230), outline =(0,0,0),width=1)
            if (c.grid[y][x].num!=None):
                Draw1.text((128+x*50, 205+y*50), str(c.grid[y][x].num),(0,0,0), font = font)
    text_all=""
    c.clues.sort(key=lambda x:x.number)
    newclue=[]
    [newclue.append(clll) for clll in c.clues if ([clll.number,clll.direction] not in [[x.number,x.direction] for x in newclue])]
    c.clues=newclue
    for i in range(len(c.clues)):
        cl=c.clues[i]
        text=cl.text
        indx=0
        while len(text[indx:])>100:
            indx+=100
            while text[indx]!=" " :
                indx+=1
                if indx==len(text):
                    text+=" "
            text=text[0:indx]+"\n"+text[indx:]
        text_all+=str(cl.number)+". "+text+" ("+ ("Across" if cl.direction=="_" else "Downwards")+").\n\n"
    Draw1.text((900,180),text_all,(0,0,0),font=font2)
    Draw1.text((50,1000),"CrossWord bot by NJ  [niyasjaman@gmail.com]",(0,0,0),font=font2)
    problem=img.copy()
    solution=img.copy()
    Draw2=ImageDraw.Draw(problem)
    Draw2.text((600,10),"PROBLEM",(200,200,200),font=font4)
    Draw3=ImageDraw.Draw(solution)
    Draw3.text((600,10),"SOLUTION",(200,200,200),font=font4)

    # str(cl.number)+". "+cl.text+" (", "Across" if cl.direction=="_" else "Downwards"+")."
    for y in range(c.size):
        for x in range(c.size):
            if (c.grid[y][x].char!="#" and c.grid[y][x].char!="|" and c.grid[y][x].char!="/" and c.grid[y][x].char!="_"): 
                Draw3.text((140+x*50, 220+y*50), c.grid[y][x].char,(100,100,100), font = font3)
    return problem,solution
if __name__=="__main__":
    with open("file.bin","rb") as file:
        c=pickle.load(file)
    p,s=Draw(c)
    p.show()
    s.show()