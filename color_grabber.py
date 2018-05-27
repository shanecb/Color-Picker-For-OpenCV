# MIT License
# 
# Copyright (c) 2018 Shane Bielefeld
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pyautogui # for getting cursor position
from mss import mss # for screenshots
import time
import tkinter as tk # for gui
from PIL import Image, ImageTk, ImageDraw # for manipulating and displaying images in gui



def convert_rgb_to_hsv(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    minVal = min(r, g, b)
    maxVal = max(r, g, b)

    h, s, v = 0, 0, 0
    v = maxVal

    delta = maxVal - minVal

    s = delta / maxVal if (maxVal != 0) else 0

    if (maxVal == minVal):
        h = 0
    else:
        if (r == maxVal):
            h = (g - b) / delta + (6 if (g < b) else 0)
        elif (g == maxVal):
            h = (b - r) / delta + 2
        else:
            h = (r - g) / delta + 4

        #h *= 60 # h between 0 and 360
        h *= 30 # h between 0 and 180
    
    if (h < 0):
        h += 180
    s *= 255 # s between 0 and 255
    v *= 255 # v between 0 and 255
    #s *= 100 # s between 0 and 100
    #v *= 100 # v between 0 and 100

    return (int(round(h)), int(round(s)), int(round(v)))


def update(root, sct, image_label, color_swatch_frame, color_value_labels):
    ## get cursor position
    x, y = pyautogui.position()
    #print('x: ' + str(x) + ', y: ' + str(y))

    ## snapshot of the area around cursor
    frame = sct.grab({ 'top': y - 5, 'left': x - 5, 'width': 11, 'height': 11 })
    img = Image.frombytes('RGB', frame.size, frame.rgb)
    img = img.resize((110, 110))
    draw = ImageDraw.Draw(img)
    draw.rectangle(((50, 50), (60, 60)), outline=200)
    img = ImageTk.PhotoImage(image=img)
    image_label.configure(image=img)
    image_label._image_cache = img # avoid garbage collection
    root.update()

    ## update color value labels
    rgb = frame.pixels[int(frame.width/2)][int(frame.height/2)]
    color_value_labels[0].configure(text='B: ' + str(rgb[2]))
    color_value_labels[1].configure(text='G: ' + str(rgb[1]))
    color_value_labels[2].configure(text='R: ' + str(rgb[0]))

    h, s, v = convert_rgb_to_hsv(rgb)
    color_value_labels[3].configure(text='H: ' + str(h))
    color_value_labels[4].configure(text='S: ' + str(s))
    color_value_labels[5].configure(text='V: ' + str(v))

    ## update color swatch
    color_swatch_frame.configure(bg='#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2]))

    root.after(20, func=lambda: update(root, sct, image_label, color_swatch_frame, color_value_labels))

## GUI Colors
WINDOW_BG_COLOR = '#%02x%02x%02x' % (236, 236, 236)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Better Digital Color Meter')
    root.configure(bg=WINDOW_BG_COLOR)

    ## create a PanedWindow in which to shape top level stuff
    pane_window = tk.PanedWindow(root, bg=WINDOW_BG_COLOR)
    pane_window.pack(fill=tk.BOTH, expand=1)

    ## left pane - image under cursor
    left_pane = tk.Frame(pane_window, width=110, height=110)#, height=110, width=140)
    left_pane.pack_propagate(0) # don't shrink
    pane_window.add(left_pane, padx=15, pady=15)

    ## create frame for image - this ensures size stays right
    image_frame = tk.Frame(left_pane, height=110, width=110, highlightthickness=0.5, highlightbackground='#%02x%02x%02x' % (218, 218, 218), bd=0)
    image_frame.pack_propagate(0) # don't shrink
    image_frame.pack()

    ## create a label for the image to sit in, but leave it empty for now
    image_label = tk.Label(image_frame)#, highlightthickness=1, highlightbackground='yellow', bd=0)
    image_label.pack(fill=tk.BOTH, expand=1)

    ## middle pane - color swatch under cursor
    middle_pane = tk.Frame(pane_window, bg=WINDOW_BG_COLOR)
    pane_window.add(middle_pane, pady=15)

    color_swatch_frame = tk.Frame(middle_pane, height=50, width=50, relief='groove', borderwidth=2)
    color_swatch_frame.pack_propagate(0) # don't shrink
    color_swatch_frame.pack()

    ## right pane - color value labels
    right_pane = tk.Frame(pane_window, bg=WINDOW_BG_COLOR)
    pane_window.add(right_pane, pady=15)

    ## create labels to display color values
    b_label = tk.Label(right_pane, text='B: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    b_label.grid(row=0, column=0, padx=(15, 0))

    g_label = tk.Label(right_pane, text='G: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    g_label.grid(row=0, column=1)

    r_label = tk.Label(right_pane, text='R: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    r_label.grid(row=0, column=2, padx=(0, 15))

    h_label = tk.Label(right_pane, text='H: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    h_label.grid(row=1, column=0, padx=(15, 0), pady=7)

    s_label = tk.Label(right_pane, text='S: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    s_label.grid(row=1, column=1, pady=7)

    v_label = tk.Label(right_pane, text='V: ', width=5, anchor='w', bg=WINDOW_BG_COLOR)
    v_label.grid(row=1, column=2, pady=7, padx=(0, 15))

    color_value_labels = [ b_label, g_label, r_label, h_label, s_label, v_label ]

    sct = mss()

    root.after(0, func=lambda: update(root, sct, image_label, color_swatch_frame, color_value_labels))
    root.mainloop()
