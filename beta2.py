import tkinter as tk

# ====== DATA ======

objects = {}
current_drag = {"id": None, "x": 0, "y": 0}


# ====== OBJECT CREATION ======

def create_object(shape):
    x, y = 300, 200

    if shape == "circle":
        obj = canvas.create_oval(x, y, x+80, y+80, fill="#3498db")

    elif shape == "square":
        obj = canvas.create_rectangle(x, y, x+80, y+80, fill="#2ecc71")

    elif shape == "rectangle":
        obj = canvas.create_rectangle(x, y, x+120, y+70, fill="#e67e22")

    objects[obj] = {
        "name": f"{shape}",
        "note": ""
    }

    canvas.tag_bind(obj, "<ButtonPress-1>", start_drag)
    canvas.tag_bind(obj, "<B1-Motion>", drag_object)
    canvas.tag_bind(obj, "<Double-Button-1>", open_editor)


# ====== DRAGGING ======

def drag_object(event):
    obj = current_drag["id"]

    dx = event.x - current_drag["x"]
    dy = event.y - current_drag["y"]

    canvas.move(obj, dx, dy)

    current_drag["x"] = event.x
    current_drag["y"] = event.y


def start_drag(event):
    current_drag["id"] = canvas.find_closest(event.x, event.y)[0]
    current_drag["x"] = event.x
    current_drag["y"] = event.y


canvas_drag_bind = start_drag


# ====== EDIT WINDOW ======

def open_editor(event):
    obj = canvas.find_closest(event.x, event.y)[0]

    window = tk.Toplevel(root)
    window.title("object")

    data = objects[obj]

    tk.Label(window, text="name").pack()

    name_entry = tk.Entry(window)
    name_entry.insert(0, data["name"])
    name_entry.pack()

    tk.Label(window, text="note").pack()

    note_text = tk.Text(window, height=5, width=30)
    note_text.insert("1.0", data["note"])
    note_text.pack()

    def save():
        data["name"] = name_entry.get()
        data["note"] = note_text.get("1.0", "end-1c")
        window.destroy()

    tk.Button(window, text="save", command=save).pack()


# ====== MENU ======

def show_menu():
    menu.post(add_button.winfo_rootx(),
              add_button.winfo_rooty() + add_button.winfo_height())


# ====== UI ======

root = tk.Tk()
root.title("arc prototype")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

# top bar
topbar = tk.Frame(root, bg="#2b2b2b", height=40)
topbar.pack(fill="x")

add_button = tk.Button(
    topbar,
    text="add object",
    command=show_menu,
    bg="#3c3c3c",
    fg="white"
)

add_button.pack(side="left", padx=5, pady=5)

# burger menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="circle", command=lambda: create_object("circle"))
menu.add_command(label="square", command=lambda: create_object("square"))
menu.add_command(label="rectangle", command=lambda: create_object("rectangle"))

# canvas
canvas = tk.Canvas(root, bg="#121212")
canvas.pack(fill="both", expand=True)

canvas.bind("<Button-1>", canvas_drag_bind)

# start
root.mainloop()