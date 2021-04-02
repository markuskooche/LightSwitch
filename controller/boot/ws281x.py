import machine, neopixel
import time


class Ws281xController:

    def __init__(self,number_of_pixels,pin_number=4):
        self.number_of_pixels = number_of_pixels
        self.pixels = neopixel.NeoPixel(machine.Pin(pin_number), number_of_pixels)
        self.pixels.write()
        self.current_rgb = (255,255,255)
        self.is_on = False

    def set_hex_color(self,hexColor):
        self.current_rgb = tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))
        self._update_state()
    
    def set_rgb_color(self ,r ,g ,b):
        self.current_rgb = (r,g,b)

    def set_is_on(self,is_on):
        self.is_on = is_on
        self._update_state()

    def _update_state(self):
        if (self.is_on):
            self._set_pixels(self.current_rgb[0],self.current_rgb[1],self.current_rgb[2])
        else:
            self._set_pixels(0,0,0)

#MARK: set colors

    def _set_pixels(self,r, g, b):
        for i in range(self.number_of_pixels):
            self.pixels[i] = (r, g, b)
        self.pixels.write()