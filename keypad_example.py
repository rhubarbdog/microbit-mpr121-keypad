# gnd rq 3.3v sda scl
import microbit as ubit 
import keypad

ubit.i2c.init()
switch = ubit.button_a

keypad = keypad.KEYPAD(ubit.i2c, ubit.pin0)
ALL_KEYS = [ j+1 for j in range(9) ] + ['*', 0, '#']

while not switch.is_pressed():

    if keypad.keypad.is_near():
        print("P", end = ' ')
    else:
        print("-", end = ' ')
                
    for i in ALL_KEYS:
        if keypad.key[i].is_pressed():
            print(str(keypad.key[i]), end = ' ')
        else:
            print('.', end = ' ')

    print('', end = '\r')
                    
    keypad.sleep(100)


print("")

for i in ALL_KEYS:
    print(i,keypad.key[i].was_pressed())
