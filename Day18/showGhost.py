# graphicsUtils.py
# ----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import sys
import math
import random
import string
import time
import types
import tkinter as tk

_root_window = None
_canvas = None
_canvas_xs = None
_canvas_ys = None
_canvas_x = None
_canvas_y = None

def formatColor(r, g, b):
	return '#%02x%02x%02x' %(int(r*255), int(g*255), int(b*255))

def _destroy_window(event = None):
	sys.exit(0)

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
	c = []
	for coord in coords:
		c.append(coord[0])
		c.append(coord[1])
	if fillColor == None:
		fillColor = outlineColor
	if filled == 0:
		fillColor = ""
	poly = _canvas.create_polygon(c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
	if behind > 0:
		_canvas.tag_lower(poly, behind=0)
	return poly


def draw_background():
	corners = [(0,0), (0, _canvas_ys), (_canvas_xs, _canvas_ys), (_canvas_xs, 0)]
	polygon(corners, _bg_color, fillColor=_bg_color, filled=True, smoothed=False)

def begin_graphics(width=604, height=480, color=formatColor(0, 0, 0), title=None):
	global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color

	if _root_window is not None:
		_root_window.destroy()

	_canvas_xs, _canvas_ys = width - 1, height - 1
	_canvas_x, _canvas_y = 0, _canvas_ys
	_bg_color = color

	_root_window = tk.Tk()
	_root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
	_root_window.title(title or 'Graphics Window')
	_root_window.resizable(0, 0)

	try:
		_canvas = tk.Canvas(_root_window, width=width, height=height)
		_canvas.pack()
		draw_background()
		_canvas.update()
	except:
		_root_window = None
		raise

	_root_window.bind( "<KeyPress>", _keypress)
	_root_window.bind( "<Button-1>", _leftclick)


def _leftclick(event):
	print("mouse left key pressed\n")

def _keypress(event):
	if event.keysym == 'Left':
		print('按下了方向鍵左鍵')
	elif event.keysym == 'Right':
		print('按下了方向鍵右鍵')
	else:
		print("%c[%x] pressed\n" %(event.char, event.keycode))

def clear_screen(background=None):
	global _canvas_x, _canvas_y
	_canvas.delete('all')
	draw_background()
	_canvas_x, _canvas_y = 0, _canvas_ys

def move_to(object, x, y=None,
	    d_o_e=lambda arg: _root_window.dooneevent,
	    d_w=tk._tkinter.DONT_WAIT):
	if y is None:
		try:
			x, y = x
		except:
			raise 'incomprehensible coordinates'

	horiz = True
	newCoords = []
	current_x, current_y = _canvas.coords(object)[0:2]
	for coord in _canvas.coords(object):
		if horiz:
			inc = x - current_x
		else:
			inc = y - current_y
		horiz = not horiz

		newCoords.append(coord + inc)

	_canvas.coords(object, *newCoords)
	d_o_e(d_w)



ghost_shape = [
	(0, 0.3),
	(0.25, 0.75),
	(0.5, 0.3),
	(0.75, 0.75),
	(0.75, -0.5),
	(0.5, -0.75),
	(-0.5, -0.75),
	(-0.75, -0.5),
	(-0.75, 0.75),
	(-0.5, 0.3),
	(-0.25, 0.75)
]

def circle(pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
	x, y = pos
	x0, x1 = x - r - 1, x + r
	y0, y1 = y - r - 1, y + r
	if endpoints == None:
		e = [0, 359]
	else:
		e = list(endpoints)
	while e[0] > e[1]: e[1] = e[1] + 360

	return _canvas.create_arc(x0, y0, x1, y1, outline=outlineColor,
			fill=fillColor, extent=e[1] - e[0], start=e[0],
			style=style, width=width)

def sleep(secs):
	global _root_window
	if _root_window == None:
		time.sleep(secs)
	else:
		_root_window.update_idletasks()
		#_root_window.after(int(1000 * secs), _root_window.quit)
		_root_window.mainloop()

def drawGhost():
	global ghost_shape

	WHITE = formatColor(1.0, 1.0, 1.0)
	BLACK = formatColor(0.0, 0.0, 0.0)

	ghost_shape = [(x * 30 + 20, y * 30 + 20) for x, y in ghost_shape]
	g = polygon(ghost_shape, formatColor(0.4, 0.13, 0.97))
	move_to(g, (50, 50))
	circle((50+30*(-0.3), 50-30*0.3), 30*0.2, WHITE, WHITE);
	circle((50+30*(0.3), 50-30*0.3), 30*0.2, WHITE, WHITE);
	circle((50+30*(-0.3), 50-30*0.3), 30*0.08, BLACK, BLACK);
	circle((50+30*(0.3), 50-30*0.3), 30*0.08, BLACK, BLACK);

if __name__ == '__main__':
	begin_graphics()
	clear_screen()
	drawGhost()
	circle((150, 150), 20, formatColor(0.3, 0.7, 0.0), formatColor(0.7, 0.3, 0.0), endpoints=[15, -15])
	sleep(2)
	
