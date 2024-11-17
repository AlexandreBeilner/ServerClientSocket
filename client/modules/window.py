from tkinter import Tk, Label, Entry, Button, PhotoImage, Frame


class Window:
    def __init__(self):
        self.window = Tk()

    def label(self,
              text,
              bg="white",
              fg="black",
              font=('Helvetica', 14),
              pady=0,
              frame=None,
              side=None,
              expand=False):
        if frame:
            label = Label(frame,
                          text=text,
                          font=font,
                          bg=bg,
                          fg=fg)
            label.pack(side=side, fill='x', expand=expand)
            return label

        label = Label(self.window,
                      text=text,
                      font=font,
                      bg=bg,
                      fg=fg)
        label.pack(pady=pady)
        return label

    def input(self,
              bg="white",
              fg="black",
              font=('Helvetica', 14),
              pady=0,
              frame=None,
              side=None,
              expand=False):
        if frame:
            entry = Entry(frame,
                          font=font,
                          bg=bg,
                          fg=fg,
                          relief="flat",  # Remove a borda padrão
                          highlightthickness=1,  # Adiciona uma borda fina
                          highlightbackground="#555",  # Cor da borda (quando não focado)
                          highlightcolor="green")  # Cor da borda ao focar
            entry.pack(side=side,
                       fill='x',
                       expand=expand,
                       pady=pady,
                       ipady=5)
            return entry

        entry = Entry(self.window,
                      font=font,
                      bg=bg,
                      fg=fg,
                      relief="flat",
                      highlightthickness=1,
                      highlightbackground="#555",
                      highlightcolor="green")
        entry.pack(pady=5, ipady=5)
        return entry

    def button(self,
               text,
               command,
               bg="white",
               fg="black",
               font=('Helvetica', 14),
               pady=0,
               padx=0,
               row=None,
               column=None,
               sticky=None,
               frame=None):
        parent = frame if frame else self.window
        button = Button(parent,
                        text=text,
                        font=font,
                        command=command,
                        bg=bg,
                        fg=fg)
        if row is not None and column is not None:
            button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        else:
            button.pack(pady=pady)
        return button

    def frame(self, bg="white", fg="black", padx=0, pady=0, row=None, column=None, sticky=None, frame=None, rowspan=1):
        parent = frame if frame is not None else self.window
        fr = Frame(parent, bg=bg)

        if row is not None and column is not None:
            fr.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan)
        else:
            fr.pack(fill="x", padx=padx, pady=pady)

        return fr

    def get(self):
        return self.window

    def create(self):
        self.window = Tk()

    def start(self):
        self.window.mainloop()

    def setup(self, title, geometry, background='white'):
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.config(background=background)

    def set_icon(self, boolean, path):
        icon = PhotoImage(file=path)
        self.window.iconphoto(boolean, icon)

    def stop(self):
        self.window.destroy()

    def grid_columnconfigure(self, column, weight):
        self.window.grid_columnconfigure(column, weight=weight)

    def grid_rowconfigure(self, row, weight):
        self.window.grid_rowconfigure(row, weight=weight)
