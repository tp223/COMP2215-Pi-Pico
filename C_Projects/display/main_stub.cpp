#include "pico_explorer.hpp"
#include "libraries/pico_display/pico_display.hpp"
#include "drivers/st7789/st7789.hpp"
#include "libraries/pico_graphics/pico_graphics.hpp"
#include "stdlib.h"
#include "drivers/button/button.hpp"

// Display driver
ST7789 st7789(PicoDisplay::WIDTH, PicoDisplay::HEIGHT, ROTATE_0, false, get_spi_pins(BG_SPI_FRONT));

// Graphics library - in RGB332 mode you get 256 colours and optional dithering for ~32K RAM.
PicoGraphics_PenRGB332 graphics(st7789.width, st7789.height, nullptr);

Button button_a(PicoDisplay::A);
Button button_b(PicoDisplay::B);
Button button_x(PicoDisplay::X);
Button button_y(PicoDisplay::Y);

// Set global width and height
int WIDTH = st7789.width;
int HEIGHT = st7789.height;

// Highlight box on screen
void highlightColour(int colour, int score) {
    
}

// Draw unselected screen
void drawDefault(int score) {
    
}

// Draw Game Over screen
void drawFailed() {
    
}

int main() {
    // Draw default screen;
    drawDefault(0);

    while(true) {
        

    }
}