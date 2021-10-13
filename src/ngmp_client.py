from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import socket
import threading
import os


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

    # Class to create a ClientSocket to receive data from a server
    class ClientSocket(socket.socket):
        def __init__(self):
            super().__init__()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.allowReceiving = False
            self.has_name = False
            self.label_text_rcvd = ""
            self.gpu_name_text = ""
            self.cpu_util_text = ""
            self.gpu_util_text = ""
            self.mem_util_text = ""
            self.gpu_temp_text = ""
            self.gpu_clock_text = ""
            self.mem_clock_text = ""
            self.gpu_fan_text = ""
            self.gpu_power_text = ""
            self.servip = []

        # Attempts to connect to the server and start receiving data
        def start_connect(self):
            try:
                if not self.allowReceiving:
                    self.sock.connect((self.servip, 25250))
                    self.allowReceiving = True
                    self.receive_data()
            except socket.error:
                messagebox.showerror("Socket Error", 'Error connecting to server. '
                                                     'Please ensure server is started before attempting to connect')

        # Attempts to receive the data from the server
        def receive_data(self):
            try:
                while self.allowReceiving:
                    bytes_received = 0
                    msg_len = 100
                    while self.allowReceiving:
                        chunk = self.sock.recv(4)
                        bytes_received = len(chunk)
                        try:
                            msg_len = int(str(chunk[1:3], 'utf-8')) + bytes_received
                        except ValueError:
                            pass
                        while bytes_received < msg_len:
                            chunk = self.sock.recv(msg_len - bytes_received)
                            if chunk != b'':
                                bytes_received = bytes_received + len(chunk)
                                chunk = str(chunk, 'utf-8')
                                self.label_text_rcvd = chunk
                                self.process_data()
                            else:
                                break
            except socket.error:
                messagebox.showerror("Socket Error", "Connection Error. Unable to receive data")

        # Takes the data received and finds which label it belongs to, (Note: gpu_name is received only once)
        # then sets the label text for the appropriate label to the value(s) of the data received
        def process_data(self):
            if self.allowReceiving:
                label_name = ""
                lab_text_len = len(self.label_text_rcvd)
                if self.label_text_rcvd.find("gpu_name") != -1 and (self.has_name is False):
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_name")
                                                                 + 12):(lab_text_len - 2)]
                    self.gpu_name_text = self.label_text_rcvd
                    self.has_name = True
                elif self.label_text_rcvd.find("cpu_util") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("cpu_util")
                                                                 + 11):(lab_text_len - 1)]
                    self.cpu_util_text = self.label_text_rcvd
                elif self.label_text_rcvd.find("gpu_util") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_util")
                                                                 + 11):(lab_text_len - 1)]
                    self.gpu_util_text = int("".join(filter(str.isdigit, self.label_text_rcvd[0:3])))
                    self.mem_util_text = int("".join(filter(str.isdigit, self.label_text_rcvd[3:])))
                elif self.label_text_rcvd.find("gpu_temp") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_temp")
                                                                 + 11):(lab_text_len - 1)]
                    self.gpu_temp_text = self.label_text_rcvd
                elif self.label_text_rcvd.find("gpu_clock") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_clock")
                                                                 + 12):(lab_text_len - 1)]
                    self.gpu_clock_text = self.label_text_rcvd
                elif self.label_text_rcvd.find("mem_clock") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("mem_clock")
                                                                 + 12):(lab_text_len - 1)]
                    self.mem_clock_text = self.label_text_rcvd
                elif self.label_text_rcvd.find("gpu_fan") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_fan")
                                                                 + 10):(lab_text_len - 1)]
                    self.gpu_fan_text = self.label_text_rcvd
                elif self.label_text_rcvd.find("gpu_power") != -1:
                    self.label_text_rcvd = self.label_text_rcvd[(self.label_text_rcvd.find("gpu_power")
                                                                 + 12):(lab_text_len - 1)]
                    self.gpu_power_text = self.label_text_rcvd
    gmp_socket = ClientSocket()

    # Class to create and configure the main widget, frames, labels, and the functions used in gathering the GPU data
    class App(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            # Configure the main window
            self.title('NVIDIA GPU MON PY Client')
            # set window height and width and position in center of screen
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
            self.socket_thread = []
            # Menu
            path = os.path.join(os.getcwd(), 'images', 'icon', 's_ico.png')
            self.load = Image.open(path)
            self.settings_icon = ImageTk.PhotoImage(self.load)
            self.menubar = Menu(master=self)
            self.client_menu = Menu(self.menubar, tearoff=0)
            self.client_menu.add_command(label="Connect to Server", command=self.start_thread)
            self.client_menu.add_command(label="Settings", image=self.settings_icon, compound="left",
                                         command=self.settings_menu)
            self.menubar.add_cascade(label="File", menu=self.client_menu)
            self.client_menu.add_separator()
            self.client_menu.add_command(label="Exit", command=self.exit_prog)
            # Frame containing the Label for the GPU Name
            # -------------------------------------------
            self.name_frame = tk.Frame(master=self, bg='black', relief='sunken', borderwidth=3)
            self.name_frame.rowconfigure(0, weight=1)
            self.name_frame.columnconfigure(0, weight=1)
            self.name_frame.grid(row=0, column=0, sticky=N+S+E+W)
            # Label containing the GPU name
            self.name_label = tk.Label(master=self.name_frame, text="", width=25, bg='black',
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

            # Configure the info Labels

            self.cpu_util_label1 = tk.Label(master=self.info_frame, text="CPU Utilization:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2,  anchor=CENTER)
            self.cpu_util_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                            bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_util_label1 = tk.Label(master=self.info_frame, text="GPU Utilization:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2,  anchor=CENTER)
            self.gpu_util_label2 = tk.Label(master=self.info_frame, text="", width=25,
                                            bg='black', fg='white', relief='sunken', borderwidth=2, anchor=CENTER)

            self.gpu_temp_label1 = tk.Label(master=self.info_frame, text="GPU Temperature:", width=25, bg='black',
                                            fg='white', relief='sunken', borderwidth=2, anchor=CENTER)
            self.gpu_temp_label2 = tk.Label(master=self.info_frame, text="{}\N{DEGREE SIGN}C"
                                            .format(""), width=25, bg='black', fg='white',
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

            # Place the appropriate labels in column 0 of the info_frame
            self.cpu_util_label1.grid(row=1, column=0, sticky=W+E)
            self.gpu_util_label1.grid(row=2, column=0, sticky=W+E)
            self.gpu_temp_label1.grid(row=3, column=0, sticky=W+E)
            self.gpu_clock_label1.grid(row=4, column=0, sticky=W+E)
            self.mem_clock_label1.grid(row=5, column=0, sticky=W+E)
            self.gpu_fan_speed_label1.grid(row=6, column=0, sticky=W+E)
            self.gpu_power_label1.grid(row=7, column=0, sticky=W+E)
            # _____________________________________________________________

            # Calls the function update_label_text() to get the info for the labels in column 1, change the text of the
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
            x = (wlx) + ((ww / 2) - (settings_w / 2))
            y = (wly) + ((wh / 2) - (settings_h / 2))
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
            gmp_socket.servip = self.servconfig.get()
            self.settings_window.destroy()

        # If receiving is enabled, label_desc will be provided by ClientSocket.process_data()
        # so that the appropriate label will be updated, otherwise the labels will use the default empty string
        # Note: name_label is configured and placed once and only once, after the name is received from the server
        def update_label_text(self):
            if gmp_socket.has_name:
                self.name_label.configure(text=gmp_socket.gpu_name_text)
                self.name_label.grid(row=0, column=0, sticky=W+E)
                gmp_socket.has_name = False
            self.cpu_util_label2.configure(text="{} %".format(gmp_socket.cpu_util_text))
            self.cpu_util_label2.grid(row=1, column=1, sticky=W + E)
            self.gpu_util_label2.configure(text="gpu: {} %, memory: {} %".format(gmp_socket.gpu_util_text,
                                                                                 gmp_socket.mem_util_text))
            self.gpu_util_label2.grid(row=2, column=1, sticky=W + E)
            self.gpu_temp_label2.configure(text="{}\N{DEGREE SIGN}C".format(gmp_socket.gpu_temp_text))
            self.gpu_temp_label2.grid(row=3, column=1, sticky=W + E)
            self.gpu_clock_label2.configure(text="{} Mhz".format(gmp_socket.gpu_clock_text))
            self.gpu_clock_label2.grid(row=4, column=1, sticky=W + E)
            self.mem_clock_label2.configure(text="{} Mhz".format(gmp_socket.mem_clock_text))
            self.mem_clock_label2.grid(row=5, column=1, sticky=W + E)
            self.gpu_fan_speed_label2.configure(text="{} %".format(gmp_socket.gpu_fan_text))
            self.gpu_fan_speed_label2.grid(row=6, column=1, sticky=W + E)
            self.gpu_power_label2.configure(text="{} Watts".format(gmp_socket.gpu_power_text))
            self.gpu_power_label2.grid(row=7, column=1, sticky=W + E)
            self.after(1000, self.update_label_text)

        # Attempt to start the thread in which the clientSocket will run
        def start_thread(self):
            try:
                self.socket_thread = threading.Thread(target=gmp_socket.start_connect)
                self.socket_thread.start()
            except RuntimeError:
                gmp_socket.start_connect()

        # Disables receiving of data, attempts to close the socket and join the thread,
        # handles any exceptions which may occur, and exits the program
        def exit_prog(self):
            gmp_socket.allowReceiving = False
            try:
                gmp_socket.close()
                self.socket_thread.join()
            except AttributeError:
                pass
            except socket.error:
                pass
            except RuntimeError:
                pass
            finally:
                self.quit()

    gpu_mon_py = App()                              # Create the App()
    gpu_mon_py.config(menu=gpu_mon_py.menubar)      # Configure the menu
    gpu_mon_py.mainloop()                           # Start the App's mainloop
    gpu_mon_py.exit_prog()                          # exit()
    return None

# Call the main()


if __name__ == "__main__":
    main()
