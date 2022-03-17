#import important library
from pathlib import Path
from tkinter import Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage,Frame,Toplevel,Label
from tkinter.constants import BOTH, LEFT, RIGHT, VERTICAL, Y

#combine important path file
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./option_all_directory")

def relative_to_assets(path: str) -> Path:
   return ASSETS_PATH / Path(path)

# define option2 --> info all directory
def option_all_directory(data):
    option_all_directory = Tk()

    option_all_directory.geometry("862x519")
    option_all_directory.configure(bg = "#3A7FF6")

    fileNames = []
    for file in data:
        fileNames.append(file[0])
    
    canvas = Canvas(
        option_all_directory,
        bg = "#3A7FF6",
        height = 519,
        width = 862,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(master=option_all_directory,
        file=relative_to_assets("button_1.png"))
    
    #quit option
    button_1 = Button(master=option_all_directory,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: option_all_directory.destroy(),
        relief="flat"
    )
    button_1.place(
        x=39.999999999999886,
        y=184.0,
        width=311.0,
        height=55.0
    )

    canvas.create_rectangle(
        39.999999999999886,
        160.0,
        211.9999999999999,
        165.0,
        fill="#FCFCFC",
        outline="")

    canvas.create_rectangle(
        430.9999999999999,
        0.0,
        861.9999999999999,
        519.0,
        fill="#FCFCFC",
        outline="")

    canvas.create_text(
        39.999999999999886,
        129.0,
        anchor="nw",
        text="Detail information partition",
        fill="#FCFCFC",
        font=("Roboto Bold", 24 * -1)
    )
    
    #data from main to this function --> get info and content
    def handle_data(data):
        after_handle = ''
        for direct in data:
            string = ''
            for line in direct:
                string += line
            after_handle += string + '\n'
        after_handle = after_handle.replace('\r','')
        #print('-----------')
        #print(after_handle)
        return after_handle
    
    h = 467.9999999999999
    l = 5.000000000000007
    
    # create all button beside directory file to read info about it
    def window_detail(text):
        window_detail = Toplevel(option_all_directory)
        Label(master=window_detail, text=text).pack(padx=30, pady=30)
    for i in range(len(fileNames)):
        canvas.create_text(
            h,
            l,
            anchor="nw",
            text=str(fileNames[i]),
            fill="#505485",
            font=("Salsa Regular", 10 * -1)
        )
            
        #temp = handle_data(data[i])
        button_i = Button(master=option_all_directory,
            #image=button_image_1,
            text = 'Info',
            borderwidth=0,
            highlightthickness=0,
            bg="yellow",
            #command=lambda i=i: print(handle_data(data[i])),
            command = lambda i=i: window_detail(handle_data(data[i])),
            relief="flat")
        button_i.place(x=h+6*len(fileNames[i])+35*fileNames[i].count('\t'),
            y=l,
            width=25,
            height=15
            )    
        if '\n' in fileNames[i]:
            l += 30

    vbar=Scrollbar(option_all_directory,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)

    option_all_directory.resizable(False, False)
    option_all_directory.mainloop()