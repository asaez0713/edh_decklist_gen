import requests
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import webbrowser

def fetch_img_url_card(commander):
    response = requests.get('https://api.scryfall.com/cards/search?q=%28type%3Acreature+type%3Alegendary%29+'+commander)

    r = response.json()

    return(r['data'][0]['image_uris']['png'])

def fetch_img_url_fullart(commander):
    response = requests.get('https://api.scryfall.com/cards/search?q=%28type%3Acreature+type%3Alegendary%29+'+commander)

    r = response.json()

    return(r['data'][0]['image_uris']['art_crop'])

commanders = []
img_class = []
titles = []
power_level = []
desc = []
urls = []

def add_info():
    commanders.append(com_entry.get())
    img_class.append(img.get())
    titles.append(title_entry.get())
    desc.append(desc_entry.get("1.0",'end-1c'))
    power_level.append(pl_entry.get())
    if img.get() == 'card':
        urls.append(fetch_img_url_card(com_entry.get()))
    else:
        urls.append(fetch_img_url_fullart(com_entry.get()))

def gen_doc(commanders,img_class,titles,power_level,desc,urls):
    f = open('commanders.html','w')

    html = """<html>
    <head>
        <title></title>
        <link rel="stylesheet" href="css/stylesheet.css"
        <meta name="robots" content="noindex">
    </head>
    <body>"""

    for i in range(len(commanders)):
        html += """
        <article>
            <div class="img">
            <img class="{0}" src="{1}">
            </div>
            <deck> {2}
            <pre>{3}
Power level: {4}
            </pre>
            </deck>
        </article>
        """.format(img_class[i],urls[i],titles[i],desc[i],power_level[i])

    html += """
    </body>
    </html>"""

    f.write(html)
    f.close()

    webbrowser.open_new_tab('commanders.html')

window = Tk()
window.title('Commander Decklist Generator')
com_lbl = Label(window, text='Commander')
com_lbl.grid(column=0,row=0,sticky=W)
com_entry = Entry(window, width=50)
com_entry.grid(column=0,row=1,sticky=W)
title_lbl = Label(window, text='Deck title')
title_lbl.grid(column=0,row=2,sticky=W)
title_entry = Entry(window, width=50)
title_entry.grid(column=0,row=3,sticky=W)
img = StringVar()
card_button = Radiobutton(window,text='Card',value='card',variable=img)
card_button.grid(column=0,row=4,sticky=W)
fullart_button = Radiobutton(window,text='Full Art',value='fullart',variable=img)
fullart_button.grid(column=0,row=4,sticky=E)
desc_lbl = Label(window,text='Brief description of deck')
desc_lbl.grid(column=0,row=5,sticky=W)
desc_entry = Text(window,width=50,height=10)
desc_entry.grid(column=0,row=6,sticky=W)
pl_lbl = Label(window, text='Power level')
pl_lbl.grid(column=0,row=7,sticky=W)
pl_entry = Entry(window, width=50)
pl_entry.grid(column=0,row=8,sticky=W)
def added():
    add_info()
    messagebox.showinfo('Success','Commander added, close this window to add another')
def gen():
    gen_doc(commanders,img_class,titles,power_level,desc,urls)
add_btn = Button(window,text='Add Commander',command=added)
add_btn.grid(column=0,row=9,sticky=W)
gen_btn = Button(window,text='Generate',command=gen)
gen_btn.grid(column=0,row=9,sticky=E)
window.mainloop()
