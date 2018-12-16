import time

class KEY:
    def __init__(self, symbol):
        self._symbol = symbol
        self._is_pressed = False
        self._was_pressed = False

    def __str__(self):
        return self._symbol

    def is_pressed(self):
        return self._is_pressed

    def was_pressed(self):
        save = self._was_pressed
        self._was_pressed = False
        return save

    def _touch(self):
        self._is_pressed = True
        self._was_pressed = True

    def _release(self):
        self._is_pressed = False

class PROXIMITY:

    def __init__(self):
        self._is_near = False
        self._was_near = False

    def is_near(self):
        return self._is_near

    def was_near(self):
        save = self._was_near
        self._was_near = False
        return save

    def _close_by(self):
        self._is_near = True
        self._was_near = True

    def _far_away(self):
        self._is_near = False


class KEYPAD:

    def __init__(self, i2c, rq_pin, address = 0x5a):
        self._i2c = i2c
        self._addr = address
        self._buf = bytearray(2)
        self._rq = rq_pin

        self._rq.set_pull(self._rq.PULL_UP)
    
        self._pad = ( KEY('1'), KEY('4'), KEY('7'), KEY('*'),
                       KEY('2'), KEY('5'), KEY('8'), KEY('0'),
                       KEY('3'), KEY('6'), KEY('9'), KEY('#') )
        self.keypad = PROXIMITY() 
        self.key = { 1 : self._pad[0],
                     2 : self._pad[4],
                     3 : self._pad[8],
                     4 : self._pad[1],
                     5 : self._pad[5],
                     6 : self._pad[9],
                     7 : self._pad[2],
                     8 : self._pad[6],
                     9 : self._pad[10],
                     0 : self._pad[7],
                     '*' : self._pad[3],
                     '#' : self._pad[11] }
        
        self._configure()
        self.switch_on()

    def sleep(self, milli_sec):
        finish = time.ticks_ms()
        if milli_sec > 0:
            finish = time.ticks_add(finish, milli_sec)
        while milli_sec <= 0 or time.ticks_diff(finish, time.ticks_ms()) > 0:
            if self._rq.read_digital() == 0:
                self._read_keys()

            if milli_sec <= 0:
                break

            time.sleep_us(50)
            
    def _configure(self):
        self.reset()

        data = b'\x2b\x01\x2c\x01\x2d\x00\x2e\x00' +\
               b'\x2f\x01\x30\x01\x31\xff\x32\x00' +\
               b'\x33\x00\x34\x00\x35\x00' +\
               b'\x36\x0f\x37\x0f\x38\x00\x39\x00' +\
               b'\x3a\x01\x3b\x01\x3c\xff\x3d\xff' +\
               b'\x3e\x00\x3f\x00\x40\x00'

        buffer_ = bytearray(2)
        for i in range(0, len(data), 2):
            buffer_[0] = data[i]
            buffer_[1] = data[i+1]
            self._i2c.write(self._addr, buffer_)

        address = 0x40
        for i in range(12):
            for datum in (10, 8): #touch/release
                address += 1
                buffer_[0] = address
                buffer_[1] = datum
                self._i2c.write(self._addr, buffer_)

        # this code was full of typo's . when repaired the keypad was less
        # functional so i've culled it
        
    def reset(self):
        self._i2c.write(self._addr, b'\x80\x63')
        
    def switch_on(self):
        self._i2c.write(self._addr, b'\x5e\xbc')

    def _read_keys(self):
        self._i2c.write(self._addr, b'\x00')
        self._buf = bytearray(self._i2c.read(self._addr, 2))
        keycode = (self._buf[1] & 0x1f) << 8 | self._buf[0]

        # keys 0 to 9 and # & *
        for i in range(12):
            mask = 0x01 << i

            if mask & keycode:
                self._pad[i]._touch()
            else:
                self._pad[i]._release()


        # proximity
        mask = 0x01 << 12

        if mask & keycode:
            self.keypad._close_by()
        else:
            self.keypad._far_away()
