import sys
import glob
import serial
import webbrowser


class Serial:
    def __init__(self, port=None, bps=9600):
        self.port = port
        self.bps = bps
        self.ser = None
        self.on_read = None

    def update(self):
        data = self.read_s()
        print(data)
        if self.on_read is not None:
            self.on_read(data)

    def onRead(self, func):
        self.on_read = func

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

    def write_s(self, command):
        self.ser.write(command)

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
