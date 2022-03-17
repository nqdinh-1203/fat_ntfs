#declare important library 
from pathlib import Path
from option_all_directory import option_all_directory
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

# combine path file
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./option_detail")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# define option1 --> option detail
def option_detail(data, all_directory):
    option_detail = Tk()

    option_detail.geometry("862x519")
    option_detail.configure(bg = "#3A7FF6")


    canvas = Canvas(master=option_detail,
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

    button_image_1 = PhotoImage(master=option_detail,
        file=relative_to_assets("button_1.png"))

    #related to option_all_directory
    def turn_all_direct(all_directory):
        option_detail.destroy()
        option_all_directory(all_directory)
    button_1 = Button(master=option_detail,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: turn_all_direct(all_directory),
        relief="flat"
    )
    button_1.place(
        x=54.999999999999886,
        y=265.0,
        width=311.0,
        height=55.0
    )

    button_image_2 = PhotoImage(master=option_detail,
        file=relative_to_assets("button_2.png"))
    
    # related to change init option
    def return_init():
        option_detail.destroy()
    button_2 = Button(master=option_detail,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: return_init(),
        relief="flat"
    )
    button_2.place(
        x=54.999999999999886,
        y=344.0,
        width=311.0,
        height=55.0
    )

    # Quiting out option detail
    button_image_3 = PhotoImage(master=option_detail,
        file=relative_to_assets("button_3.png"))
    button_3 = Button(master=option_detail,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: option_detail.destroy(),
        relief="flat"
    )
    button_3.place(
        x=54.999999999999886,
        y=423.0,
        width=311.0,
        height=55.0
    )

    canvas.create_text(
        39.999999999999886,
        127.0,
        anchor="nw",
        text="WELCOME TO MY APP!",
        fill="#FCFCFC",
        font=("Roboto Bold", 24 * -1)
    )

    canvas.create_text(
        481.9999999999999,
        74.0,
        anchor="nw",
        text="Detail information partition",
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
        text="OPTIONS :",
        fill="#FCFCFC",
        font=("Quicksand Bold", 22 * -1)
    )
    
    if len(data) == 8:
        canvas.create_text(
            481.9999999999999,
            163.0,
            anchor="nw",
            text=f"This is a FAT32 Disk !!!\n\nBytes per Sector: {data[0]}\nSectors per Cluster: {data[1]}\nReserved Sector: {data[2]}\nNumber of FAT: {data[3]}\nEntries of RDET: {data[4]}\nTotal Sectors in Volume: {data[5]}\nSectors per FAT: {data[6]}\nFirst Cluster of RDET: {data[7]}",
            fill="#505485",
            font=("Salsa Regular", 21 * -1)
        )
    else: 
        canvas.create_text(
            481.9999999999999,
            163.0,
            anchor="nw",
            text=f"This is a NTFS Disk !!!\n\nBytes per Sector: {data[0]}\nSectors per Cluster: {data[1]}\nNumber of Sector/Track: {data[2]}\nNumber of Disk Side: {data[3]}\nStart Sector of Disk: {data[4]}\nTotal Sector Of Disk: {data[5]}\nStart Cluster of MFT: {data[6]}\nStart Cluster of MFT Mirror: {data[7]}\nSize of MFT Entry:{data[8]}\nVolume Serial Number: \n{data[9]}",
            fill="#505485",
            font=("Salsa Regular", 21 * -1)
        )
    option_detail.resizable(False, False)
    option_detail.mainloop()
