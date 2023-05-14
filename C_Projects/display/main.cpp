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
    // Set backlight
    st7789.set_backlight(200);

    // background colour
    graphics.set_pen(0, 0, 0);
    graphics.clear();

    // Draw four boxes (red, green, blue, yellow)
    if (colour == 0) {
        graphics.set_pen(255, 0, 0);
    } else {
        graphics.set_pen(100, 0, 0);
    }
    Rect red_rect(0, 0, WIDTH/2, HEIGHT/2);
    graphics.rectangle(red_rect);

    if (colour == 1) {
        graphics.set_pen(0, 255, 0);
    } else {
        graphics.set_pen(0, 100, 0);
    }
    Rect green_rect(WIDTH/2, 0, WIDTH/2, HEIGHT/2);
    graphics.rectangle(green_rect);

    if (colour == 2) {
        graphics.set_pen(0, 0, 255);
    } else {
        graphics.set_pen(0, 0, 100);
    }
    Rect blue_rect(0, HEIGHT/2, WIDTH/2, HEIGHT/2);
    graphics.rectangle(blue_rect);

    if (colour == 3) {
        graphics.set_pen(255, 255, 0);
    } else {
        graphics.set_pen(100, 100, 0);
    }
    Rect yellow_rect(WIDTH/2, HEIGHT/2, WIDTH/2, HEIGHT/2);
    graphics.rectangle(yellow_rect);

    graphics.set_pen(0, 0, 0);
    Rect score_rect(WIDTH-35, 5, 30, 20);
    graphics.rectangle(score_rect);

    // write some text inside the box with 10 pixels of margin
    // automatically word wrapping
    red_rect.deflate(10);
    graphics.set_pen(0, 0, 0);
    graphics.text("A", Point(red_rect.x, red_rect.y), red_rect.w);

    green_rect.deflate(10);
    graphics.set_pen(0, 0, 0);
    graphics.text("X", Point(green_rect.x, green_rect.y), green_rect.w);

    blue_rect.deflate(10);
    graphics.set_pen(0, 0, 0);
    graphics.text("B", Point(blue_rect.x, blue_rect.y), blue_rect.w);

    yellow_rect.deflate(10);
    graphics.set_pen(0, 0, 0);
    graphics.text("Y", Point(yellow_rect.x, yellow_rect.y), yellow_rect.w);

    score_rect.deflate(3);
    graphics.set_pen(255, 255, 255);
    char scoreStr[5];
    sprintf(scoreStr, "%d", score);
    graphics.text(scoreStr, Point(score_rect.x, score_rect.y), score_rect.w);

    // Update screen
    st7789.update(&graphics);
}

// Draw unselected screen
void drawDefault(int score) {
    highlightColour(4, score);
}

// Draw Game Over screen
void drawFailed() {
    st7789.set_backlight(200);

    // background colour
    graphics.set_pen(255, 0, 0);
    graphics.clear();

    graphics.set_pen(150, 0, 0);
    graphics.text("GAME OVER", Point(50, 40), 50, 4.0);

    st7789.update(&graphics);
}

int main() {
    // Draw default screen;
    drawDefault(0);

    // List of current pattern
    int currentNumbers[99];
    int currentLocation = 0;
    bool passedRound = false;
    bool failed = false;
    int currentInput = 0;

    sleep_ms(1000);

    while(true) {
        sleep_ms(500);
        if (failed) {
            currentLocation = 0;
            passedRound = false;
            failed = false;
            currentInput = 0;
            drawFailed();
            sleep_ms(2000);
            drawDefault(0);
        }

        // Random number between 0 and 3
        currentNumbers[currentLocation] = rand() % 4;

        for (int i=0; i<=currentLocation; i++) {
            highlightColour(currentNumbers[i], currentLocation);
            sleep_ms(1000);
            drawDefault(currentLocation);
            sleep_ms(100);
        }

        passedRound = false;
        currentInput = 0;

        while (!passedRound && !failed) {
            if (button_a.raw()) {
                highlightColour(0, currentLocation);
                while (button_a.raw());
                drawDefault(currentLocation);
                if (currentNumbers[currentInput] == 0) {
                    currentInput++;
                } else {
                    failed = true;
                }
            }
            if (button_x.raw()) {
                highlightColour(1, currentLocation);
                while (button_x.raw());
                drawDefault(currentLocation);
                if (currentNumbers[currentInput] == 1) {
                    currentInput++;
                } else {
                    failed = true;
                }
            }
            if (button_b.raw()) {
                highlightColour(2, currentLocation);
                while (button_b.raw());
                drawDefault(currentLocation);
                if (currentNumbers[currentInput] == 2) {
                    currentInput++;
                } else {
                    failed = true;
                }
            }
            if (button_y.raw()) {
                highlightColour(3, currentLocation);
                while (button_y.raw());
                drawDefault(currentLocation);
                if (currentNumbers[currentInput] == 3) {
                    currentInput++;
                } else {
                    failed = true;
                }
            }
            if (currentInput - 1 == currentLocation && !failed) {
                passedRound = true;
            }
        }

        if (!failed) {
            currentLocation++;
            drawDefault(currentLocation);
        }

    }
}