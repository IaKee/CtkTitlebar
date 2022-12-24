import ctypes
from tkinter import Tk, Button, Menu, Frame, Label, X, Y, TOP, RIGHT, LEFT
from winreg import HKEY_CURRENT_USER as hkey, QueryValueEx as getSubkeyValue, OpenKey as getKey
from ctypes.wintypes import DWORD, BOOL, HRGN, HWND
from PIL import Image, ImageTk
from os import getcwd

user32 = ctypes.windll.user32
dwm = ctypes.windll.dwmapi
class ACCENTPOLICY(ctypes.Structure):
	_fields_ = [
		("AccentState", ctypes.c_uint),
		("AccentFlags", ctypes.c_uint),
		("GradientColor", ctypes.c_uint),
		("AnimationId", ctypes.c_uint)
	]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
	_fields_ = [
		("Attribute", ctypes.c_int),
		("Data", ctypes.POINTER(ctypes.c_int)),
		("SizeOfData", ctypes.c_size_t)
	]
SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute.argtypes = (HWND, WINDOWCOMPOSITIONATTRIBDATA)
SetWindowCompositionAttribute.restype = ctypes.c_int

def HEXtoRGBAint(HEX):
    alpha = HEX[7:]
    blue = HEX[5:7]
    green = HEX[3:5]
    red = HEX[1:3]

    gradientColor = alpha + blue + green + red
    return int(gradientColor, base = 16)
    
def blur(hwnd, hexColor = False, Acrylic = False, Dark = False, AccentState = 3):
	accent = ACCENTPOLICY()
	accent.AccentState = 3
	gradientColor = 0
		
	if Acrylic:
		accent.AccentState = AccentState
		if hexColor == False:
			accent.AccentFlags = 2
			gradientColor = HEXtoRGBAint('#91203801')
	
			accent.GradientColor = gradientColor

	data = WINDOWCOMPOSITIONATTRIBDATA()
	data.Attribute = 19
	data.SizeOfData = ctypes.sizeof(accent)
	data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int))
	SetWindowCompositionAttribute(int(hwnd), data)	
	if Dark: 
		data.Attribute = 26
		SetWindowCompositionAttribute(int(hwnd), data)
        
def theme():
    valueMeaning = {0: "Dark", 1: "Light"}
    try:
        key = getKey(hkey, "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
        subkey = getSubkeyValue(key, "AppsUseLightTheme")[0]
    except FileNotFoundError:
        return None
    return valueMeaning[subkey]

def isDark():
    if theme() is not None:
        return theme() == 'Dark'

class Tk(Tk):
	def __init__(self):
		super().__init__()
		path = getcwd()
		path += "\\assets\\"

		self._t0_load = Image.open(path + '\\close_50.png')
		self._t0_img = ImageTk.PhotoImage(self._t0_load)
		self._t0_hov_load = Image.open(path + '\\close_100.png')
		self._t0_hov_img = ImageTk.PhotoImage(self._t0_hov_load)

		self._t1_load = Image.open(path + '\\minisize_50.png')
		self._t1_img = ImageTk.PhotoImage(self._t1_load)
		self._t1_hov_load = Image.open(path + '\\minisize_100.png')
		self._t1_hov_img = ImageTk.PhotoImage(self._t1_hov_load)

		self._t2_load = Image.open(path + '\\fullwin_50.png')
		self._t2_img = ImageTk.PhotoImage(self._t2_load)
		self._t2_hov_load = Image.open(path + '\\fullwin_100.png')
		self._t2_hov_img = ImageTk.PhotoImage(self._t2_hov_load)

		self._t3_load = Image.open(path + '\\togglefull_50.png')
		self._t3_img = ImageTk.PhotoImage(self._t3_load)
		self._t3_hov_load = Image.open(path + '\\togglefull_100.png')
		self._t3_hov_img = ImageTk.PhotoImage(self._t3_hov_load)
				
		self.w, self.h = 265, 320
		self.o_flag = False
		self.o_m = False
		self.o_f = False
		self.colors = {
			"Light": "#ffffff",
			"Dark": "#2b2b2b",
			"button_activebg": '#262626',
			"button_activefg": '#262626',
			"exit_fg": "#e81123",
			"exit_bg": "#e81123",
			"dark": "#000000",
			"dark_nf": "#2b2b2b",
			"light": "#f2efef",
			"light_nf": "#f2efef",
			"dark_bg": "#202020"
		}
		self.theme = "light"
		self.bg = self.colors["light"]
		self.nf = self.colors["light_nf"]
		self.fg = "dark"
		
		if isDark():
			self.theme = "dark"
			self.bg = self.colors["dark"]
			self.nf = self.colors["dark_nf"]
			self.fg = "light"
		
		if self.theme == "dark":
			self["background"] = self.colors["dark_bg"]

		self.popup = Menu(self, tearoff = 0)
		self.popup.add_command(label = "还原", command = self.resizeback)
		self.popup.entryconfig("还原", state="disabled")
		self.popup.add_command(label = "最小化", command = self.minsize)
		self.popup.add_command(label = "最大化", command = self.maxsize)
		self.popup.add_separator()
		self.popup.add_command(label = "关闭 (Alt+F4)", command = self.destroy)
		
		self.titlebar = Frame(self, bg = self.bg, bd = 0)
		self._titleicon = Label(self.titlebar, bg = self.bg)
		self._titletext = Label(self.titlebar, text = "tk", bg = self.bg, fg = self.colors[self.fg])
		self._titlemin = Button(self.titlebar, bg = self.bg)
		self._titlemax = Button(self.titlebar, bg = self.bg)
		self._titleexit = Button(self.titlebar, bg = self.bg)
		
		self._titleexit.config(bd = 0,
			activeforeground = self.colors["exit_fg"],
			activebackground = self.colors["exit_bg"],
			width = 44,
			image = self._t0_hov_img,
			relief = 'flat',
			command = self.quit
		)
		self._titlemin.config(bd = 0,
			activeforeground = self.colors["button_activefg"],
			activebackground = self.bg,
			width = 44,
			image = self._t1_hov_img,
			relief = 'flat',
			command = self.minsize
		)
		self._titlemax.config(bd = 0,
			activeforeground = self.colors["button_activefg"],
			activebackground = self.bg,
			width = 44,
			image = self._t2_hov_img,
			relief = 'flat',
			command = self.maxsize
		)

		self._titleicon.pack(fill = Y, side = LEFT, padx = 6, pady = 6)
		self._titletext.pack(fill = Y, side = LEFT, padx = 1, pady = 1)

		self._titleexit.pack(fill = Y, side = RIGHT)
		self._titlemax.pack(fill = Y, side = RIGHT)
		self._titlemin.pack(fill = Y, side = RIGHT)

		self.titlebar.pack(fill = X, side = TOP)
		
		# binds & after
		self.bind("<FocusOut>", self.focusout)
		self.bind("<FocusIn>", self.focusin)
		self.bind("<F11>", self.maxsize)

		self._titleexit.bind("<Enter>", self.exit_on_enter)
		self._titleexit.bind("<Leave>", self.exit_on_leave)
		self._titlemin.bind("<Enter>", self.min_on_enter)
		self._titlemin.bind("<Leave>", self.min_on_leave)
		self._titlemax.bind("<Enter>", self.max_on_enter)
		self._titlemax.bind("<Leave>", self.max_on_leave)
		
		self._titleicon.bind("<Button-3>", self.popupmenu)
		self.titlebar.bind("<ButtonPress-1>", self.dragging)
		self.titlebar.bind("<ButtonRelease-1>", self.stopping)
		self.titlebar.bind("<B1-Motion>", self.moving)
		self.titlebar.bind("<Double-Button-1>", self.maxsize)
		
		self.geometry("%sx%s" % (self.w, self.h))
		self.after(1000, self.check) # low cpu use
		
	def addblur(self):
		if self.theme == "dark":
			hwnd = ctypes.windll.user32.GetForegroundWindow()
			#blur(hwnd = hwnd, Dark = True, Acrylic = True, AccentState = 3) # Custom AccentState
	
	def popupmenu(self, event):
		self.popup.post(event.x_root, event.y_root)
	
	def dragging(self, event):
		global x, y
		self.config(cursor = "fleur")
		x = event.x
		y = event.y

	def stopping(self, event):
		x = None
		y = None

	def moving(self, event):
		global x, y
		if self.o_m:
			self.resizeback()
		else:
			self.config(cursor = "arrow")
			deltax = event.x - x
			deltay = event.y - y
			self.geometry("+%s+%s" % (self.winfo_x() + deltax, self.winfo_y() + deltay))
			self.update()
			
	def focusout(self, event):
		if self.theme != "light":
			self.o_f = True
			self.titlebar["bg"] = self.nf
			self._titleicon["bg"] = self.nf
			self._titletext["bg"] = self.nf, 
			self._titlemin["bg"] = self.nf
			self._titlemax["bg"] = self.nf
			self._titleexit["bg"] = self.nf
	
	def focusin(self, event):
		if self.theme != "light":
			self.o_f = False
			self.titlebar["bg"] = self.bg
			self._titleicon["bg"] = self.bg
			self._titletext["bg"] = self.bg
			self._titlemin["bg"] = self.bg
			self._titlemax["bg"] = self.bg
			self._titleexit["bg"] = self.bg

	def resizeback(self):
		self.popup.entryconfig("还原", state = "disabled")
		self.popup.entryconfig("最大化", state = "active")
		self.wm_geometry("%dx%d+%d+%d" % (int(self.w), int(self.h), int(self.w_x), int(self.w_y)))
		self._titlemax["command"] = self.maxsize
		self._titlemax["image"] = self._t2_hov_img
		self.o_m = False
	
	def maxsize(self, event = None):
		self.config(cursor = "arrow")
		if event and self.o_m == True:
			self.resizeback()
		else:
			self.popup.entryconfig("还原", state = "active")
			self.popup.entryconfig("最大化", state = "disabled")
			self.w_x, self.w_y = self.winfo_x(), self.winfo_y()
			self.o_m = True
			self._titlemax["image"] = self._t3_hov_img
			self._titlemax["command"] = self.resizeback
			w, h = self.wm_maxsize()
			self.geometry("%dx%d+0+0" % (w, h - 40))
	
	def minsize(self):
		self.overrideredirect(False)
		self.o_flag = False
		self.state("iconic")
		
	def check(self):
		if self.state() != "iconic" and self.o_flag == False:
			self.overrideredirect(True)
			self.o_flag = True
			self.addblur()
			
		self.after(1200, self.check) # low cpu use
	
	def exit_on_enter(self, event):
		if not self.o_f:
			self._titleexit["background"] = self.colors["exit_fg"]
			self._titleexit["image"] = self._t0_img
		else:
			pass
			
	def exit_on_leave(self, event):
		if not self.o_f:
			self._titleexit["background"] = self.bg
			self._titleexit["image"] = self._t0_hov_img
		else:
			pass
		
	def min_on_enter(self, event):
		self._titlemin["image"] = self._t1_img

	def min_on_leave(self, event):
		self._titlemin["image"] = self._t1_hov_img

	def max_on_enter(self, event):
		if not self.o_m:
			self._titlemax["image"] = self._t2_img
		else:
			self._titlemax["image"] = self._t3_img

	def max_on_leave(self, event):
		if not self.o_m:
			self._titlemax["image"] = self._t2_hov_img
		else:
			self._titlemax["image"] = self._t3_hov_img
	
	def title(self, text):
		self._titletext["text"] = text
	
	def iconbitmap(self, photo):
		self._icon = Image.open(photo)
		self._icon = self._icon.resize((16, 16)) 
		self._img = ImageTk.PhotoImage(self._icon)
		self._titleicon["image"] = self. _img
	
	def geometry(self, size):
		if self.w and self.h:
			pass
		else:
			self.w, self.h = size.split('x')[0], size.split('x')[1]
		self.wm_geometry(size)

if __name__ == "__main__":
	example = Tk()
	example.mainloop()
