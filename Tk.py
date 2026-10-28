# uncompyle6 version 3.9.3
# Python bytecode version base 3.4 (3310)
# Decompiled from: Python 3.11.2 (main, May 12 2026, 05:17:27) [GCC 12.2.0]
# Embedded file name: C:\Users\Majhrs\Documents\Majhrs\__init__.py
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import askyesno as AskYesNo, showerror as MsgErr, showinfo as MsgInfo, showwarning as MsgWarning
from tkinter.simpledialog import askstring as AskStr, askinteger as AskInt, askfloat as AskFloat
from Majhrs.Shell import *
import os
_Tk = Tk
_Text = Text
_Menu = Menu
Str, Float, Int = StringVar, DoubleVar, IntVar
_Button = Button
for Obj in (Frame, Button, Entry, Label, ttk.Frame, ttk.Button, ttk.Entry, ttk.Label):
    Obj.__enter__ = lambda self: self
    Obj.__exit__ = lambda *Args, self: None

class Tk(_Tk):
    __ver__ = "b1.8.4"

    def __init__(self, *Args, **Kw):
        _Tk.__init__(self, *Args)
        self.Title("Tk")
        self.Size("400x400")
        self.Size(CENTER)
        for k, _v in sorted({"ver": (lambda v: setattr(self, "__ver__", v)),  "title": (lambda v: self.Title(v)), 
         "icon": (self.Icon),  "resize": (lambda v: self.resizable(*v)), 
         "size": (self.Size)}.items(), reverse=1):
            if k in Kw:
                _v(Kw.pop(k, None))
                continue

        self.bind_all("Alt+F4", (lambda e: self.Exit() and self.Exit()))
        self.protocol("WM_DELETE_WINDOW", (lambda : self.Exit() and self.Exit()))
        self._Exit = False

    def __enter__(self):
        return self

    def __exit__(self, *Args):
        self.mainloop()

    def Icon(self, p=None, Default=None):
        if p:
            try:
                _Tk.iconbitmap(self, p, Default)
            except:
                pass

        else:
            _Tk.iconbitmap()

    def Title(self, s=None, Ver=True):
        if s:
            if Ver:
                if self.__ver__:
                    s += " - " + self.__ver__
            return _Tk.title(self, s)

    def Size(self, s=None):
        if s:
            if s == CENTER:
                s = "{}x{}+{}+{}".format(self.winfo_width(), self.winfo_height(), round(self.winfo_screenwidth() / 2 - self.winfo_width() / 2), round(self.winfo_screenheight() / 2 - self.winfo_height() / 2))
            _Tk.geometry(self, s)
        else:
            s = _Tk.geometry(self)
        self.update()
        return s

    def Exit(self, Force=False):
        if Force or self._Exit:
            self.destroy()
            self.quit()
            sys.exit()
        else:
            self._Exit = AskYesNo(None, "¿Salir?")
        return self._Exit

    def MenuBar(self, *Args, **Kw):
        try:
            self.MB.delete(0, END)
        except AttributeError:
            self["menu"] = self.MB = Menu(self, *Args, **Kw)

        return self.MB


class Button(_Button):

    def flash(self, *Args):
        for Relief in (SUNKEN, RAISED):
            self["relief"] = Relief
            self.after(16)
            self.update()

    def invoke(self, *Args):
        self.flash()
        _Button.invoke(self)


class Text(_Text):

    def __init__(self, Master=None, **Kw):
        self.F1 = ttk.Frame(Master)
        _Text.__init__(self, self.F1, **Kw)
        self.SB1 = ttk.Scrollbar(self.F1, command=self.yview)
        self["yscrollcommand"] = self.SB1.set
        self.SB1.pack(fill=Y, side=RIGHT)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        for m in (vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()).difference(vars(Text).keys()):
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.F1, m))
                continue

    def __enter__(self):
        return self

    def __exit__(self, *Args):
        return


class ScrolledFrame(ttk.Frame):

    def __init__(self, Master):
        self.C1 = Canvas(Master)
        ttk.Frame.__init__(self, self.C1)
        self._X = self._Y = False

    def __enter__(self):
        return self

    def __exit__(self, *Args):
        self.bind("<Configure>", (lambda e: self.C1.config(scrollregion=self.C1.bbox(ALL))))
        self.C1.create_window((0, 0), window=self, anchor=NW)
        if not self._Y + self._X:
            self.Horizontal()
            self.Vertical()
        self.C1.pack(fill=BOTH, expand=1)

    def Horizontal(self):
        self._X = not self._X
        if self._X:
            self.SB2 = ttk.Scrollbar(self.C1.master, orient=HORIZONTAL, command=self.C1.xview)
            self.C1["xscrollcommand"] = self.SB2.set
            SB2.pack(fill=X, side=BOTTOM)
        else:
            self.C1["xscrollcommand"] = None
            self.SB2.destroy()

    def Vertical(self):
        self._Y = not self._Y
        if self._Y:
            self.SB["state"] = NORMAL
            self.SB1 = ttk.Scrollbar(self.C1.master, command=self.C1.yview)
            self.C1["yscrollcommand"] = self.SB1.set
            self.SB1.pack(fill=Y, side=RIGHT)
        else:
            self.SB1["state"] = DISABLED


class Menu(_Menu):

    def __init__(self, Master, *Args, **Kw):
        self._Master = Master
        self.Kw = {"label": (Kw.get("title", "(Sin Titulo)")),  "command": (Kw.pop("command", None)),  "menu": self}
        _Menu.__init__(self, (Master.widget if isinstance(Master, Event) else Master), *Args, **Kw)

    def __enter__(self):
        return self

    def __exit__(self, *Args):
        e = self._Master
        if isinstance(e, Event):
            self["tearoff"] = 0
            return self.post(e.x_root, e.y_root)
        del e
        try:
            self.master.add_cascade(**self.Kw)
        except AttributeError:
            pass


MenuContext = Menu
if __name__ == "__main__":
    with Tk() as self:
        with Text(self, bg="black", fg="white", insertbackground="white", wrap=WORD) as T1:
            T1.focus()
            T1.pack(fill=BOTH, expand=1)

# okay decompiling __init__.pyo
