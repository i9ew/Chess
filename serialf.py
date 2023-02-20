import sys
import glob
import serial
from constants import *
from functions import *
from time import sleep


class Serial:
    def __init__(self, port=None, bps=9600):
        self.port = port
        self.bps = bps
        self.ser = None
        self.on_read = self.activated
        clear_file(serial_input_path)
        clear_file(serial_output_path)

    def update(self):
        sleep(0.1)
        data = self.read_s()
        if data is not None:
            data = data.decode()
            print(f"Serial: {data}")
            if self.on_read is not None:
                self.on_read(data)

        poped = pop_string_from_file(serial_input_path)
        if poped is not None:
            print(poped)
            self.write_s(poped)

    def onRead(self, func):
        self.on_read = func

    def activated(self, x):
        append_string_to_file(serial_output_path, x)

    def init_port(self):
        if self.port is None:
            av_p = self.serial_ports()
            while av_p is None or av_p == []:
                av_p = self.serial_ports()
            self.ser = self.opens(port=av_p[0])
            self.port = av_p[0]
            print(f"Serial connected {self.port}")
        else:
            self.ser = self.opens(port=self.port)

    def run(self):
        self.init_port()
        while True:
            self.update()

    def write_s(self, command):
        self.ser.write(command.encode())

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def opens(self, port="COM4", bps=9600, timex=5):
        try:
            # Откройте последовательный порт
            ser = serial.Serial(port, bps, timeout=timex)

            if ser.is_open:
                global SERIAL_IS_OPEN
                SERIAL_IS_OPEN = True
                # print("--- последовательный порт открыт ---")
                return ser

        except Exception as e:
            print("--- Открытое исключение ---:", e)
            return None

    def read_s(self, code="utf-16"):
        if self.ser.in_waiting:
            st = self.ser.read(self.ser.in_waiting)
            return st
        else:
            return None
