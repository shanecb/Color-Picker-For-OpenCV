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

## takes a tuple with the r, g, and b values on a 0-255 scale, and returns a
## tuple with the h value on a 0-180 scale, and the s and v values on a 0-255
## scale
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

