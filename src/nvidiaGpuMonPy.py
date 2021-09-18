from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import psutil
import pynvml
import socket
import threading


# __MAIN__


def main():

    # Dictionary for the border effects around the frames and labels
    border_effects = {
        "flat": tk.FLAT,
        "sunken": tk.SUNKEN,
        "raised": tk.RAISED,
        "groove": tk.GROOVE,
        "ridge": tk.RIDGE,
    }

    # Initialize NVML and get the GPU handle which is used by NVML to get the GPU info
    pynvml.nvmlInit()
    _handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    # Class to create and configure the main widget, frames, labels, and the functions used in gathering the GPU data
    class App(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_thread = threading.Thread(target=self.start_server)     # start the server on a separate thread
            self.allowSending = False   # sending off by default
            self.disconnect = False     # used to stop the server
            self.has_name = False
            # Configure the main window
            self.title('NVIDIA GPU MON PY')
            # Set window height and width and position in center of screen
            w = 320
            h = 180
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = (sw / 2) - (w / 2)
            y = (sh / 2) - (h / 2)
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))
            self.resizable(False, False)
            self.configure(bg='black')
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=0)
            # Settings window

            # File menu
            self.menubar = Menu(master=self)
            self.load = Image.open("images\\icon\\s_ico.png")
            self.settings_icon = ImageTk.PhotoImage(self.load)
            self.server_menu = Menu(self.menubar, tearoff=0)
            self.server_menu.add_command(label="Start Server", command=self.server_thread.start)
            self.server_menu.add_command(label="Settings", image=self.settings_icon, compound="left",
                                         command=self.settings_menu)
            self.menubar.add_cascade(label="File", menu=self.server_menu)
            self.server_menu.add_separator()
            self.server_menu.add_command(label="Exit", command=self.exit)

            # Frame containing the Label for the GPU Name
            # -------------------------------------------
            self.name_frame = tk.Frame(master=self, bg='black', relief='sunken', borderwidth=3)
            self.name_frame.rowconfigure(0, weight=1)
            self.name_frame.columnconfigure(0, weight=1)
            self.name_frame.grid(row=0, column=0, sticky=N+S+E+W)
            # Label containing the GPU name
            self.name_label = tk.Label(master=self.name_frame, text=self.get_gpu_name(), width=25, bg='black',
                                       fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.name_label.grid(row=0, column=0, sticky=W+E)
            # ___________________________________________

            # Frame containing the Labels for the remaining GPU information
            # _____________________________________________________________
            self.info_frame = tk.Frame(master=self, bg='black', relief='sunken', borderwidth=3)
            self.info_frame.rowconfigure(1, weight=1)
            self.info_frame.columnconfigure(0, weight=1)
            self.info_frame.rowconfigure(5, weight=1)
            self.info_frame.columnconfigure(1, weight=1)
            self.info_frame.grid(row=1, column=0, sticky=N+S+E+W)
            # configure the info Labels
            self.cpu_util_label1 = tk.Label(master=self.info_frame, text="CPU Utilization:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.cpu_util_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                            bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_util_label1 = tk.Label(master=self.info_frame, text="GPU Utilization:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2,  anchor=CENTER)
            self.gpu_util_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                            bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_temp_label1 = tk.Label(master=self.info_frame, text="GPU Temperature:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_temp_label2 = tk.Label(master=self.info_frame, text="{}\N{DEGREE SIGN}C"
                                            .format(self.get_gpu_temps()), width=25, bg='black', fg='white',
                                            relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_clock_label1 = tk.Label(master=self.info_frame, text="GPU Clock Speed:", width=25, bg='black',
                                             fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_clock_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                             bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            self.mem_clock_label1 = tk.Label(master=self.info_frame, text="Memory Clock Speed:", width=25, bg='black',
                                             fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.mem_clock_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                             bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_fan_speed_label1 = tk.Label(master=self.info_frame, text="GPU Fan Speed:", width=25, bg='black',
                                                 fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_fan_speed_label2 = tk.Label(master=self.info_frame, text="", width=25, bg='black', fg='white',
                                                 relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_power_label1 = tk.Label(master=self.info_frame, text="GPU Power:", width=25, bg='black',
                                             fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_power_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                             bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            # place the appropriate labels in column 0 of the info_frame
            self.cpu_util_label1.grid(row=1, column=0, sticky=W+E)
            self.gpu_util_label1.grid(row=2, column=0, sticky=W+E)
            self.gpu_temp_label1.grid(row=3, column=0, sticky=W+E)
            self.gpu_clock_label1.grid(row=4, column=0, sticky=W+E)
            self.mem_clock_label1.grid(row=5, column=0, sticky=W+E)
            self.gpu_fan_speed_label1.grid(row=6, column=0, sticky=W+E)
            self.gpu_power_label1.grid(row=7, column=0, sticky=W+E)
            # _____________________________________________________________

            # calls the function update_label_text() to get the info for the labels in column 1, change the text of the
            # appropriate label and places the labels in column 1 of info_frame
            # Note: A separate function was needed here in order to regularly update the information every 1 second
            #       with .after()

            self.update_label_text()

        def settings_menu(self):
            self.settings_window = Toplevel()
            self.settings_window.title('Settings')
            self.settings_window.resizable(False, False)
            self.settings_window.attributes("-topmost", 1)
            settings_w = 240
            settings_h = 50
            wlx = self.winfo_x()
            wly = self.winfo_y()
            ww = self.winfo_width()
            wh = self.winfo_height()
            x = (wlx) + ((ww/2)-(settings_w/2))
            y = (wly) + ((wh/2)-(settings_h/2))
            self.settings_window.geometry("%dx%d+%d+%d" % (settings_w, settings_h, x, y))
            self.settings_window.configure(bg='black')
            self.settings_window.columnconfigure(0, weight=1)
            self.settings_window.rowconfigure(0, weight=0)
            self.ipconfiglabel = Label(master=self.settings_window, text="Server ip: ", width=10, bg='black',
                                       fg='white', borderwidth=2, anchor=CENTER)
            self.servconfig = Entry(master=self.settings_window, insertbackground='white', width=25, bg='black',
                                    fg='white', relief='sunken', borderwidth=2)
            self.servconfig.focus_set()
            self.done_button = Button(master=self.settings_window, text='Done', command=self.get_serv_config)
            self.ipconfiglabel.grid(row=0, column=0, sticky=W + E)
            self.servconfig.grid(row=0, column=1, sticky=W + E)
            self.done_button.grid(row=1, column=1)

        def get_serv_config(self):
            self.servip = self.servconfig.get()
            self.settings_window.destroy()

        # Gets the current gpu values every second and updates the appropriate label text
        # if allowSending is true then the data is sent using send_data()
        def update_label_text(self):
            new_text = []
            for i in self.info_frame.children.values():
                if i == self.cpu_util_label2:
                    new_text.insert(0, psutil.cpu_percent())
                    self.cpu_util_label2.configure(text="{} %".format(new_text[0]))
                    self.cpu_util_label2.grid(row=1, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "cpu_util")
                        self.send_data(new_text)

                elif i == self.gpu_util_label2:
                    new_text = self.get_gpu_utilization_rates()
                    self.gpu_util_label2.configure(text=new_text[0])
                    self.gpu_util_label2.grid(row=2, column=1, sticky=W+E)
                    if self.allowSending:
                        util_data = []
                        util_data.insert(0, new_text[0].memory)
                        util_data.insert(0,new_text[0].gpu)
                        util_data.insert(0, "gpu_util")
                        self.send_data(util_data)
                elif i == self.gpu_temp_label2:
                    new_text = self.get_gpu_temps()
                    self.gpu_temp_label2.configure(text="{}\N{DEGREE SIGN}C".format(new_text[0]))
                    self.gpu_temp_label2.grid(row=3, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "gpu_temp")
                        self.send_data(new_text)
                elif i == self.gpu_clock_label2:
                    new_text = self.get_gpu_clock_speed()
                    self.gpu_clock_label2.configure(text="{} Mhz".format(new_text[0]))
                    self.gpu_clock_label2.grid(row=4, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "gpu_clock")
                        self.send_data(new_text)
                elif i == self.mem_clock_label2:
                    new_text = self.get_mem_clock_speed()
                    self.mem_clock_label2.configure(text="{} Mhz".format(new_text[0]))
                    self.mem_clock_label2.grid(row=5, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "mem_clock")
                        self.send_data(new_text)
                elif i == self.gpu_fan_speed_label2:
                    new_text = self.get_gpu_fan_speed()
                    self.gpu_fan_speed_label2.configure(text="{} %".format(new_text[0]))
                    self.gpu_fan_speed_label2.grid(row=6, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "gpu_fan")
                        self.send_data(new_text)
                elif i == self.gpu_power_label2:
                    new_text = self.get_gpu_power_usage()
                    self.gpu_power_label2.configure(text="{} Watts".format(new_text[0]))
                    self.gpu_power_label2.grid(row=7, column=1, sticky=W+E)
                    if self.allowSending:
                        new_text.insert(0, "gpu_power")
                        self.send_data(new_text)
            self.after(1000, self.update_label_text)

        # Uses the handle to get the gpu name and return it

        def get_gpu_name(self):
            self.gpu_name = []
            self.name = pynvml.nvmlDeviceGetName(_handle)
            self.gpu_name.append(self.name)
            return self.gpu_name[0]

        # Gets and returns the utilization rates of the GPU and video memory
        def get_gpu_utilization_rates(self):
            self.util_rates = []
            self.util = pynvml.nvmlDeviceGetUtilizationRates(_handle)
            self.util_rates.append(self.util)
            return self.util_rates

        # Gets and returns the GPU temperature in degrees celsius
        def get_gpu_temps(self):
            self.gpu_temps = []
            self.temps = pynvml.nvmlDeviceGetTemperature(_handle, 0)
            self.gpu_temps.append(self.temps)
            return self.gpu_temps

        # Gets and returns the GPU clock speed in Mhz
        def get_gpu_clock_speed(self):
            self.gpu_clock_speed = []
            self.gpu_clock = pynvml.nvmlDeviceGetClockInfo(_handle, 0)
            self.gpu_clock_speed.append(self.gpu_clock)
            return self.gpu_clock_speed

        # Gets and returns the memory clock speed in Mhz
        def get_mem_clock_speed(self):
            self.gpu_mem_clock = []
            self.mem_clock = pynvml.nvmlDeviceGetClockInfo(_handle, 2)
            self.gpu_mem_clock.append(self.mem_clock)
            return self.gpu_mem_clock

        # Gets and returns the fan speed as a percentage
        def get_gpu_fan_speed(self):
            self.gpu_fan_speed = []
            self.fan_speed = pynvml.nvmlDeviceGetFanSpeed(_handle)
            self.gpu_fan_speed.append(self.fan_speed)
            return self.gpu_fan_speed

        # Gets and returns the GPU current power usage in watts
        def get_gpu_power_usage(self):
            self.gpu_power_usage = []
            self.power = pynvml.nvmlDeviceGetPowerUsage(_handle)   # nvml value is returned as milliwatts
            self.power = round(self.power/1000)  # convert from milliwatts to watts and round
            self.gpu_power_usage.append(self.power)
            return self.gpu_power_usage

        # Executes when the server thread is started via the file menu "Start Server" choice
        def start_server(self):
            self.sock.bind((self.servip, 25250))
            self.sock.listen(1)
            try:
                print("Server Started.")
                self.connection, self.client_ip = self.sock.accept()
                self.allowSending = True
                self.prep_gpu_name()
            except OSError:
                pass

        # Gets the gpu name ready to be sent to the client
        def prep_gpu_name(self):
            device_name = []
            device_name.append(str(self.get_gpu_name(), 'utf-8'))
            device_name.insert(0, "gpu_name")
            self.send_data(device_name)

        # Handles sending the data and any exceptions which may occur
        def send_data(self, new_text):
            data = []
            total_sent = 0
            data = bytearray((str(new_text)), 'utf-8')
            msg_len = len(data)
            new_text.insert(0, msg_len)
            data = bytearray((str(new_text)), 'utf-8')
            while total_sent < len(data) and self.allowSending:
                try:
                    sent = self.connection.send(data[total_sent:])
                    total_sent += sent
                except ConnectionResetError:
                    messagebox.showerror("Connection Error", "Connection error. Connection was lost.")
                    self.allowSending = False
                except ConnectionAbortedError:
                    messagebox.showerror("Connection Error", "Connection error. Connection was lost.")
                    self.allowSending = False
            return None

        # Closes the socket, joins the thread (if possible), and quits the program
        def stop_server(self):      # Disabled for now
            self.allowSending = False
            self.disconnect = True
            self.sock.shutdown(socket.SHUT_RDWR)
            self.exit()

        # File menu exit choice
        def exit(self):
            self.sock.close()
            if not self.disconnect:
                self.allowSending = False
                if self.server_thread.is_alive():
                    self.server_thread.join()
                self.quit()
            else:
                self.disconnect = False

    gpu_mon_py = App()                              # Create the App()
    gpu_mon_py.config(menu=gpu_mon_py.menubar)      # Configure the menu
    gpu_mon_py.mainloop()                           # Start the App's mainloop
    gpu_mon_py.exit()                               # exit()
    pynvml.nvmlShutdown()                           # Shutdown pynvml
    return None

# Call the main()


if __name__ == "__main__":
    main()
