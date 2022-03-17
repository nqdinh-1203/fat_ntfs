#import important library
from pathlib import Path
from option_detail import option_detail
from option_all_directory import option_all_directory
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#combine path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./control_option")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#defind function controll get_detail, get all director, ....
def getElement(data, all_directory):
    control_option = Tk()

    control_option.geometry("862x519")
    control_option.configure(bg = "#3A7FF6")


    canvas = Canvas(master=control_option,
        bg = "#3A7FF6",
        height = 519,
        width = 862,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        430.9999999999999,
        0.0,
        861.9999999999999,
        519.0,
        fill="#FCFCFC",
        outline="")

    button_image_1 = PhotoImage(master=control_option,
        file=relative_to_assets("button_1.png"))

    # return to choose directory
    button_1 = Button(master=control_option,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: return_init(),
        relief="flat"
    )
    button_1.place(
        x=481.9999999999999,
        y=344.0,
        width=311.0,
        height=55.0
    )

    button_image_2 = PhotoImage(master=control_option,
        file=relative_to_assets("button_2.png"))
    
    #combined to option_detail --> detail
    button_2 = Button(master=control_option,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: option_detail(data, all_directory),
        relief="flat"
    )
    button_2.place(
        x=481.9999999999999,
        y=147.0,
        width=311.0,
        height=55.0
    )

    button_image_3 = PhotoImage(master=control_option,
        file=relative_to_assets("button_3.png"))
    
    #related to option_all_directory --> all directory
    button_3 = Button(master=control_option,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: option_all_directory(all_directory),
        relief="flat"
    )
    
    button_3.place(
        x=481.9999999999999,
        y=247.0,
        width=311.0,
        height=55.0
    )

    canvas.create_text(
        39.999999999999886,
        127.0,
        anchor="nw",
        text="WELCOME TO MY APP!",
        fill="#FCFCFC",
        font=("Quicksand", 24 * -1)
    )

    canvas.create_text(
        481.9999999999999,
        74.0,
        anchor="nw",
        text="OPTIONS",
        fill="#505485",
        font=("Roboto Bold", 24 * -1)
    )

    canvas.create_rectangle(
        39.999999999999886,
        160.0,
        99.99999999999989,
        165.0,
        fill="#FCFCFC",
        outline="")

    canvas.create_text(
        39.999999999999886,
        193.0,
        anchor="nw",
        text="PLEASE CHOOSE OPTIONS",
        fill="#FCFCFC",
        font=("Quicksand Bold", 22 * -1)
    )

    canvas.create_text(
        39.999999999999886,
        260.0,
        anchor="nw",
        text="This project made by:\nHuynh Quoc Duy\nLe Thanh Loc\nNguyen Quang Dinh\nPham Duc Huy\n",
        fill="#FCFCFC",
        font=("Quicksand Regular", 21 * -1)

    )
    #To change path in init window
    def return_init():
        from gui import init_window
        control_option.destroy()
        init_window()

    control_option.resizable(False, False)
    control_option.mainloop()