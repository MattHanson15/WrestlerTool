import tkinter
from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from datetime import date 

searchUrl = "https://www.cagematch.net/?id=2&view=workers&search="
search = 0

#Search Function
def findWrestler():
    global search
    listResults.delete(1,END)
    searchString = entryText.get().replace(" ","+")
    page = requests.get(searchUrl+searchString, headers={'Accept-Encoding': 'identity'})
    soup = BeautifulSoup(page.content, 'html.parser')
    search = soup.findAll(True, {'class':['TRow1', 'TRow2']})
    for result in search:
        row = result.findAll('td')
        name = row[2].text.ljust(30)
        home = row[4].text.ljust(42)
        try:
            birthday = row[3].text.split('.')
            today = date.today()
            age = (today.year - int(birthday[2]) - ((today.month, today.day) < (int(birthday[1]), int(birthday[0]))))
        except:
            age = "  "
        try:
            promotion = row[7].find('img').get('title')
        except:
            promotion = " "
        listResults.insert(END, name+str(age)+"  "+home+promotion)
        
#More Info Function
def moreInfo():
    selected = listResults.curselection()
    if(selected[0] > 0):
        i = 0
        infoUrl = "https://www.cagematch.net/"+search[selected[0]-1].find('a')['href']
        page = requests.get(infoUrl, headers={'Accept-Encoding': 'identity'})
        soup = BeautifulSoup(page.content, 'html.parser')
        name = status = alias = age = gender = home = height = weight = training = promotion = brand = role = ""
        name = soup.find(class_='TextHeader').text
        labelInfoName.configure(text=name, font="bolded")
        status = "("+soup.findAll(class_='TextSubHeader')[0].text+")"
        labelInfoStatus.configure(text=status)
        try:
            alias = soup.findAll(class_='TextSubHeader')[1].text
            labelInfoAlias.configure(text=alias)
        except:
            labelInfoAlias.configure(text="Also known as")
        data = soup.findAll(class_='InformationBoxTable')
        if(status == "(Active)"):
            for row in data[0]:
                if("Age:" in row.text):
                    age = row.text.split(':')[1].split('s')[0]+" old"
                elif("Promotion:" in row.text):
                    promotion = row.text.split(':')[1]
                    if(promotion == "Freelancer"):
                        promotion = "Currently Independent"
                    else:
                        promotion = "Currently works for "+promotion
                elif("Brand:" in row.text):
                    brand = row.text.split(':')[1]
                elif("Active Roles:" in row.text):
                    role = row.text.split(':')[1]
            if(brand != ""):
                promotion += "("+brand+")"
            if(role != ""):
                promotion += " as "+role
        elif(status == "(Inactive)"):
            i = 1
            age = listResults.get(selected)[30:33]+" year old"
            promotion = "Currently Retired"
        elif(status == "(Deceased)"):
            i = 1
            for row in data[0]:
                if("Day of death:" in row.text):
                    age = row.text.split(':')[1].split('f')[1].split(' ')[1].split(')')[0]+" year old(at time of death)"
            promotion = "Deceased"
        for row in data[1-i].findAll(class_='InformationBoxRow'):
            if("Gender" in row.text):
                gender = row.text.split(':')[1]
            elif("Birthplace" in row.text):
                home = row.text.split(':')[1]
            elif("Height" in row.text):
                height = row.text.split(':')[1].split('(')[0]
            elif("Weight" in row.text):
                weight = row.text.split(':')[1].split('(')[0]
        for row in data[2-i].findAll(class_='InformationBoxRow'):
            if "Trainer:" in row.text:
                training = row.text.split(':')[1]
        labelInfoAge.configure(text=age+" "+gender+" from "+home)
        labelInfoHeight.configure(text=height+"tall "+"and weighs "+weight)
        labelInfoWork.configure(text=promotion)
        labelInfoExp.configure(text="Trained by "+training)
        
#Main Window
window = tkinter.Tk()
window.title("Wrestler Tool")
window.geometry("800x600")
frame = ttk.Frame(window)
frame.columnconfigure(0, weight=0)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=0)
frame.columnconfigure(3, weight=1)

#Search Bar
labelName = Label(frame, text="Name:")
labelName.grid(row=0, column=0)
entryText = Entry(frame)
entryText.grid(row=0, column=1)
buttonSearch = Button(frame, text="Search", command=findWrestler)
buttonSearch.grid(row=0, column=2)
listResults=Listbox(frame, width=100, font="TkFixedFont")
listResults.grid(row=1, column=0, pady=(50,0), columnspan=4)
listResults.insert(0, "Gimmick                       Age    Home                                    Promotion")

#Info Area
buttonInfo = Button(frame, text="More Info", command=moreInfo)
buttonInfo.grid(row=2, column=0, sticky=W)
labelInfoName = Label(frame)
labelInfoName.grid(row=3, column=0, sticky=W)
labelInfoAlias = Label(frame, wraplength=800, justify="left")
labelInfoAlias.grid(row=4, column=0, sticky=W, columnspan=4)
labelInfoStatus = Label(frame)
labelInfoStatus.grid(row=3, column=1, sticky=W)
labelInfoAge = Label(frame)
labelInfoAge.grid(row=5, column=0, sticky=W, columnspan=4)
labelInfoHeight = Label(frame)
labelInfoHeight.grid(row=6, column=0, sticky=W, columnspan=4)
labelInfoWork = Label(frame)
labelInfoWork.grid(row=7, column=0, sticky=W, columnspan=4)
labelInfoExp = Label(frame)
labelInfoExp.grid(row=8, column=0, sticky=W, columnspan=4)

frame.pack()
#Main Loop
window.mainloop()