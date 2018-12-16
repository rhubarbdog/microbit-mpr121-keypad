<h1>mpr121 keypad</h1>

`keypad.py` defines one class `KEYPAD` for user programs.  The class has 3 parameters `i2c` (the i2c bus to use), `rq_pin` (the requset pin) and `address` (the i2c device address, this will be 0x5a, 0x5b, 0x5c or 0x5d).</br>
The `KEYPAD` object is made up of 2 types of object.  12 `KEY` objects which are accessed via the dictionary `KEYPAD.key` using the symbol on the keypad as the lookup symbol. And a `PROXIMITY` object (`KEYPAD.keypad`).</br>
The `PROXIMITY` object has 2 user methods
<table>
<tr><td>Method</td><td>Type</td></tr>
<tr><td><code>.is_near()</code></td><td>boolean</td><td>is a finger near the keypad.</td></tr>
<tr><td><code>.was_near()</code></td><td>boolean</td><td>has anything been near the keypad since the <code>.was_near()</code> method was last executed.</td></tr>
</table>
`KEY` objects have 2 user methods
<table>
<tr><td>Method</td><td>Type</td></tr>
<tr><td><code>.is_pressed()</code></td><td>boolean</td><td>returns True if the key is being pressed.</td></tr>
<tr><td><code>.was_pressed()</code></td><td>boolean</td><td>returns True if the key has been pressed since the last call to the <code>.was_pressed()</code> method.</td></tr>
</table>

Object `KEYPAD` has 1 user method, `keypad.sleep` this polls the keypad and should be called frequently. Do not use `microbit.sleep` or `time.sleep`. `keypad.sleep` has millisecond precision so for times shorter than that use `time.sleep_us`.  If your program has no need for sleep regular calls to `keypad.sleep(0)` is required to log key presses.  KEY states and PROXIMITY to the sensor are accessed by methods on the dictionay `KEYPAD.key` or object `KEYPAD.keypad`.
