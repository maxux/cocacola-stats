import TermTk as ttk
import requests

# fridge screen terminal size: 145 x 42

root = ttk.TTk()

logo = [
    """         __                              ___   __        .ama     ,""",
    """      ,d888a                          ,d88888888888ba.  ,88"I)   d """,
    """     a88']8i                         a88".8"8)   `"8888:88  " _a8' """,
    """   .d8P' PP                        .d8P'.8  d)      "8:88:baad8P'  """,
    """  ,d8P' ,ama,   .aa,  .ama.g ,mmm  d8P' 8  .8'        88):888P'    """,
    """ ,d88' d8[ "8..a8"88 ,8I"88[ I88' d88   ]IaI"        d8[           """,
    """ a88' ]P "bm8mP8'(8'.8I  8[      d88'    `"         .88            """,
    """,88I ]P[  .I'.8     88' ,8' I[  ,88P ,ama    ,ama,  d8[  .ama.g    """,
    """[88' I8, .I' ]8,  ,88B ,d8 aI   (88',88"8)  d8[ "8. 88 ,8I"88[     """,
    """]88  `8888"  '8888" "88P"8m"    I88 88[ 8[ ]P "bm8m88[.8I  8[      """,
    """]88,          _,,aaaaaa,_       I88 8"  8 ]P[  .I' 88 88' ,8' I[   """,
    """`888a,.  ,aadd88888888888bma.   )88,  ,]I I8, .I' )88a8B ,d8 aI    """,
    '''  "888888PP"'        `8""""""8   "888PP'  `8888"  `88P"88P"8m"     '''
]

index = 0
for line in logo:
    ttk.TTkLabel(parent=root, pos=(40, 3 + index), text=line)
    index += 1

ttk.TTkLabel(parent=root, pos=(65, 17), text="⣏⡉ ⡀⣀ ⠄ ⢀⣸ ⢀⡀ ⢀⡀   ⢎⡑ ⣰⡀ ⢀⣀ ⣰⡀ ⠄ ⢀⣀ ⣰⡀ ⠄ ⢀⣀ ⢀⣀")
ttk.TTkLabel(parent=root, pos=(65, 18), text="⠇  ⠏  ⠇ ⠣⠼ ⣑⡺ ⠣⠭   ⠢⠜ ⠘⠤ ⠣⠼ ⠘⠤ ⠇ ⠭⠕ ⠘⠤ ⠇ ⠣⠤ ⠭⠕")

state = {
    "consumers": [],
    "items": [],
}

@ttk.pyTTkSlot()
def hello():
    for a in state["consumers"]:
        print(a.checkState())

    for a in state["items"]:
        print(a.checkState())

webdata = requests.get("http://10.241.0.240:7922/info")
info = webdata.json()

# print(info)

line = 22
for consumer in info["consumers"]:
    label = f" {consumer[1]}"
    checked = (line == 22)

    radio = ttk.TTkRadioButton(parent=root, text=label, pos=(40, line), size=(20, 1), radiogroup="consumer", checked=checked)
    state["consumers"].append(radio)

    line += 1

line = 22
for item in info["items"]:
    label = f" {item[1]} ({item[2]} cl)"
    checked = (line == 22)

    radio = ttk.TTkRadioButton(parent=root, text=label, pos=(80, line), size=(30, 1), radiogroup="items", checked=checked)
    state["items"].append(radio)

    line += 1

drink = ttk.TTkButton(parent=root, pos=(60, 35),  size=(30, 5), border=True, text="Take a Drink")
drink.clicked.connect(hello)

root.mainloop()
