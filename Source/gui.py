#declare library
import mainFAT32
import mainNTFS
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#set path file
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def init_window():
    window = Tk()

    #define detail information option
    def option_detail(name):
        with open(f'\\\\.\\{name}:', "rb") as fr:
            data = fr.read(512)
        if chr(data[3]) == 'N':
            vbr = mainNTFS.VBR(name)
            get_info = vbr.get_info()

            all_directory = mainNTFS.get_store_all_directory(vbr,name)
        else: 
            get_info = mainFAT32.BootSector(name).get_info()

            create_fat = mainFAT32.FAT32(name)

            all_directory = mainFAT32.get_store_all_directory(2, 0, create_fat, name, '')
            
        window.destroy()

        from control_option import getElement
        getElement(get_info, all_directory)

    window.geometry("567x568")
    window.configure(bg = "#3C91E6")
    canvas = Canvas(
        window,
        bg = "#3C91E6",
        height = 568,
        width = 567,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        43.0,
        83.0,
        anchor="nw",
        text="Hey There !",
        fill="#FAFFFD",
        font=("ZCOOLXiaoWei Regular", 64 * -1)
    )

    canvas.create_text(
        43.0,
        167.0,
        anchor="nw",
        text="Enter you directory",
        fill="#FAFFFD",
        font=("ZCOOLXiaoWei Regular", 36 * -1)
    )

    entry_image_1 = PhotoImage(master=window,
        file=relative_to_assets("entry_1.png"))

    canvas.create_image(
        225.0,
        304.0,
        image=entry_image_1
    )
    entry_1 = Entry(master=window,
        bd=0,
        bg="#FAFFFD",
        highlightthickness=0
    )
    entry_1.place(
        x=51.0,
        y=281.0,
        width=348.0,
        height=44.0
    )

    canvas.create_text(
        43.0,
        251.0,
        anchor="nw",
        text="Name directory (Please wait it's still running)",
        fill="#FAFFFD",
        font=("ZCOOLXiaoWei Regular", 18 * -1)
    )
    button_image_1 = PhotoImage(master=window,
        file=relative_to_assets("button_1.png"))
    
    #related to detail option
    button_1 = Button(master=window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command= lambda: option_detail(entry_1.get().upper()),
        relief="flat"
    )
    button_1.place(
        x=43.0,
        y=375.0,
        width=158.0,
        height=46.0
    )
    window.resizable(False, False)
    window.mainloop()

init_window()