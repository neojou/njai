
import sys
import math
import random
import string
import time
import types
import tkinter as tk

_root_window = None

def formatColor(r, g, b):
	return '#%02x%02x%02x' %(int(r*255), int(g*255), int(b*255))

def begin_graphics(width=604, height=480, color=formatColor(0, 0, 0), title=None):
	global _root_window

	if _root_window is not None:
		_root_window.destroy()

	_root_window = tk.Tk()
	_root_window.title(title or 'Graphics Window')

	_root_window.bind( "<KeyPress>", _keypress)
	_root_window.bind( "<Button-1>", _leftclick)
	_root_window.mainloop()


def _leftclick(event):
	print("mouse left key pressed\n")

def _keypress(event):
	if event.keysym == 'Left':
		print('按下了方向鍵左鍵')
	elif event.keysym == 'Right':
		print('按下了方向鍵右鍵')
	else:
		print("%c[%x] pressed\n" %(event.char, event.keycode))

if __name__ == '__main__':
	begin_graphics()

