import TermTk as ttk
import requests

# fridge screen terminal size: 145 x 42 // 79 x 24

baseurl = "http://10.241.0.240:7922"
root = ttk.TTk()

"""
logo = []
with open("logo", "r") as f:
    content = f.read()
    logo = content.split("\n")

index = 0
for line in logo:
    ttk.TTkLabel(parent=root, pos=(40, 3 + index), text=line)
    index += 1

ttk.TTkLabel(parent=root, pos=(65, 17), text="⣏⡉ ⡀⣀ ⠄ ⢀⣸ ⢀⡀ ⢀⡀   ⢎⡑ ⣰⡀ ⢀⣀ ⣰⡀ ⠄ ⢀⣀ ⣰⡀ ⠄ ⢀⣀ ⢀⣀")
ttk.TTkLabel(parent=root, pos=(65, 18), text="⠇  ⠏  ⠇ ⠣⠼ ⣑⡺ ⠣⠭   ⠢⠜ ⠘⠤ ⠣⠼ ⠘⠤ ⠇ ⠭⠕ ⠘⠤ ⠇ ⠣⠤ ⠭⠕")
"""

state = {
    "consumers": [],
    "items": [],
}

remote = {
    "consumers": [],
    "items": [],
}

@ttk.pyTTkSlot()
def hello():
    consumer = None
    item = None

    for id, value in enumerate(state["consumers"]):
        if value.checkState() == 2:
            consumer = remote["consumers"][id][0]

    for id, value in enumerate(state["items"]):
        if value.checkState() == 2:
            item = remote["items"][id][0]

    requests.get(f"{baseurl}/consume/{consumer}/{item}")

    state["consumers"][0].setCheckState(True)
    state["items"][0].setCheckState(True)

webdata = requests.get(f"{baseurl}/info")
info = webdata.json()

line = 2
for consumer in info["consumers"]:
    remote["consumers"].append(consumer)

    label = f" {consumer[1]}"
    checked = (line == 22)

    radio = ttk.TTkRadioButton(parent=root, text=label, pos=(10, line), size=(20, 1), radiogroup="consumer", checked=checked)
    state["consumers"].append(radio)

    line += 1

line = 2
for item in info["items"]:
    remote["items"].append(item)

    label = f" {item[1]} ({item[2]} cl)"
    checked = (line == 22)

    radio = ttk.TTkRadioButton(parent=root, text=label, pos=(40, line), size=(30, 1), radiogroup="items", checked=checked)
    state["items"].append(radio)

    line += 1

drink = ttk.TTkButton(parent=root, pos=(24, 18),  size=(30, 5), border=True, text="Take a Drink")
drink.clicked.connect(hello)

# auto select first items
state["consumers"][0].setCheckState(True)
state["items"][0].setCheckState(True)

root.mainloop()
