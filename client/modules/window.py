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
            entry = Entry(frame, font=font, bg=bg, fg=fg)
            entry.pack(side=side,
                       fill='x',
                       expand=expand,
                       pady=pady)
            return entry

        entry = Entry(self.window, font=font, bg=bg, fg=fg)
        entry.pack(pady=5)
        return entry

    def button(self,
               text,
               command,
               bg="white",
               fg="black",
               font=('Helvetica', 14),
               pady=0):
        button = Button(self.window,
                        text=text,
                        font=font,
                        command=command,
                        bg=bg,
                        fg=fg)
        button.pack(pady=pady)
        return button

    def frame(self, bg="white", fg="black", padx=0, pady=0, side=None):
        fr = Frame(self.window, bg=bg)
        fr.pack(fill="x", padx=padx, pady=pady, side=side)
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
