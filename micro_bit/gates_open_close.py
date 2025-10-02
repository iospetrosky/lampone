def on_button_pressed_a():
    global moving, index
    if not (moving):
        moving = True
        basic.show_leds("""
            . . . # .
            . . # . .
            . # . . .
            # . . . .
            # # # # #
            """)
        index = 90
        while index <= 180:
            pins.servo_write_pin(AnalogPin.P2, index)
            basic.pause(30)
            index += 1
        moving = False
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global moving, angle2
    if not (moving):
        moving = True
        basic.show_leds("""
            . . . . .
            . . . . .
            . . . . .
            # # # # #
            # # # # #
            """)
        angle2 = 180
        while angle2 >= 90:
            pins.servo_write_pin(AnalogPin.P2, angle2)
            basic.pause(30)
            angle2 = angle2 - 1
        moving = False
input.on_button_pressed(Button.B, on_button_pressed_b)

angle2 = 0
index = 0
moving = False
basic.show_icon(IconNames.SMALL_DIAMOND)
pins.servo_write_pin(AnalogPin.P2, 90)

def on_forever():
    pass
basic.forever(on_forever)
