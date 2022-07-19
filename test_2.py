# no class

import gi, serial, time
import serial.tools.list_ports

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

arduino_port = None

for port in serial.tools.list_ports.comports():
    if port.pid == 0x7523 and port.vid == 0x1a86:
        arduino_port = port.device

if arduino_port is None:
    raise ValueError('Device not found')

ser = serial.Serial()
ser.port = arduino_port
ser.baudrate = 115200
ser.timeout = 1
ser.open()

def read_i2c_addr():
    pass

def actuate_relay_1(relay_1):
    ser.write(b'\x30')

def actuate_relay_2(relay_2):
    ser.write(b'\x31')

def read_adc_1(adc_1):
    ser.write(b'\x32')
    # i2c controller sends three bytes, higher byte/lower byte/carriage return
    a = b''
    while True:
        b = ser.read(1)
        if  int.from_bytes(b, 'little') == 0x0D:
            break
        a += b
    # assemble higher/lower byte into integer
    adc_reading = a[1]|a[0]<<8
    # convert to voltage (4.84 is measured at VREF pin on Arduino)
    adc_volt = adc_reading * 4.84 / 1024
    # print to label on button press
    adc_value_1.set_text(f'{adc_volt:.3f}V')

def main():
    pass

app = Gtk.Window(title="I2C Automated Testing")

app.set_border_width(10)

panel1 = Gtk.Frame()
panel2 = Gtk.Frame(label="Relay")
panel3 = Gtk.Frame(label="ADC")
        # panel4 = Gtk.Frame()

panel1.set_label_align(0.5,0.5)
panel2.set_label_align(0.5,0.5)
panel3.set_label_align(0.5,0.5)
        # panel4.set_label_align(0.5,0.5)

panel1.set_shadow_type(Gtk.ShadowType.NONE)
# panel2.set_shadow_type(Gtk.ShadowType.NONE)
# panel3.set_shadow_type(Gtk.ShadowType.NONE)
# panel4.set_shadow_type(Gtk.ShadowType.NONE)

        # panel1.connect("clicked", on_button_clicked)
        # panel2.connect("clicked", on_button_clicked)
        # panel3.connect("clicked", on_button_clicked)
        # panel4.connect("clicked", on_button_clicked)

grid = Gtk.Grid(column_homogeneous=True,row_homogeneous=True,column_spacing=10,row_spacing=10)

grid.attach(panel1,0,0,1,2)
grid.attach(panel2,1,0,3,1)
grid.attach(panel3,1,1,3,1)
# grid.attach(panel4,1,1,1,1)

app.add(grid)

#####################################################################################################
read_i2c_addr = Gtk.Button(label="Read I2C Address")
i2c_addr = Gtk.Label(label="I2C Address:")

grid_1 = Gtk.Grid(column_homogeneous=True,row_homogeneous=True,column_spacing=10,row_spacing=10)

grid_1.attach(read_i2c_addr,0,0,1,1)
grid_1.attach(i2c_addr,0,1,1,1)

panel1.add(grid_1)

relay_1 = Gtk.Button(label="Relay 1")
relay_2 = Gtk.Button(label="Relay 2")
relay_3 = Gtk.Button(label="Relay 3")
relay_1.connect("clicked", actuate_relay_1)
relay_2.connect("clicked", actuate_relay_2)
relay_status_1 = Gtk.Label(label="OFF")
relay_status_2 = Gtk.Label(label="OFF")
relay_status_3 = Gtk.Label(label="OFF")

#####################################################################################################
grid_2 = Gtk.Grid(column_homogeneous=True,row_homogeneous=True,column_spacing=10,row_spacing=10)

grid_2.attach(relay_1,0,0,1,1)
grid_2.attach(relay_2,1,0,1,1)
grid_2.attach(relay_3,2,0,1,1)
grid_2.attach(relay_status_1,0,1,1,1)
grid_2.attach(relay_status_2,1,1,1,1)
grid_2.attach(relay_status_3,2,1,1,1)
panel2.add(grid_2)

adc_1 = Gtk.Button(label="ADC 1")
adc_2 = Gtk.Button(label="ADC 2")
adc_3 = Gtk.Button(label="ADC 3")
adc_1.connect("clicked", read_adc_1)
adc_value_1 = Gtk.Label(label="0.000V")
adc_value_2 = Gtk.Label(label="0.000V")
adc_value_3 = Gtk.Label(label="0.000V")

#####################################################################################################
grid_3 = Gtk.Grid(column_homogeneous=True,row_homogeneous=True,column_spacing=10,row_spacing=10)

grid_3.attach(adc_1,0,0,1,1)
grid_3.attach(adc_2,1,0,1,1)
grid_3.attach(adc_3,2,0,1,1)
grid_3.attach(adc_value_1,0,1,1,1)
grid_3.attach(adc_value_2,1,1,1,1)
grid_3.attach(adc_value_3,2,1,1,1)
panel3.add(grid_3)



app.set_size_request(750,750)
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()

    # while True:
    #     arduino.write(b'hell world!')
    #     time.sleep(1)

# if __name__ == "__main__":
#     main()