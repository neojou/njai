import tkinter as tk

_root_window = None

def begin_graphics(width=604, height=480, title=None):
	global _root_window

	if _root_window is not None:
		_root_window.destroy()

	_root_window = tk.Tk()
	_root_window.title(title or 'Graphics Window')
	_root_window.mainloop()

if __name__ == '__main__':
	begin_graphics()

