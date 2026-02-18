from pympler import muppy
all_objects = muppy.get_objects()  # this causes pydev debugger exit with code -1073741819 (0xC0000005)

import faulthandler
faulthandler.enable()

import serial
import serial.tools.list_ports
from customtkinter import *
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
import time
from random import randint

class A():

    def com_connect(self, *args):
        try:
            self.com = self.combobox.get().upper()
            if "ARDUINO UNO" in self.com:
                self.com = self.com[-5:-1]
            self.arduino = serial.Serial(port=f'{str(self.com)}', baudrate=9600, timeout=.1)
            self.arduino.close()
            self.arduino.open()
            messagebox.showinfo("Notify!", "Serial connected!")
            self.isConnect = True
            self.com_label.configure(text=f"Connection state [Connected]", text_color="green")
            self.connect_button.configure(text="Disconnect", text_color="red", fg_color="black")
        except:
            if self.isConnect:
                messagebox.showwarning("Notify!", "Serial disconnected!!")
                self.arduino.close()
                self.connect_button.configure(text="Connect", text_color="white", fg_color="green")
                self.com_label.configure(text=f"Connection state [Disconnected]", text_color="red")
            else:
                messagebox.showerror("Error", "Select a valid COM port!!")

    def Gui(self):
        self.top = CTk()
        self.top.title("A.M.S.V.C")
        self.top.resizable(False, False)
        self.top.geometry()

        self.frame1 = CTkFrame(self.top, corner_radius=15)
        self.frame1.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        portat = list(serial.tools.list_ports.comports())
        ports = []
        ports.append("COM2")
        for p in portat:
            ports.append(str(p))

        self.com_label = CTkLabel(self.frame1, text=f"Connection state [Unavailable]",
                                  font=("cairo", 14, "bold"), text_color="blue", width=250)
        self.com_label.pack( pady=10, padx=15)

        self.combobox = CTkOptionMenu(self.frame1, values=ports)
        self.combobox.pack( padx=20, pady=10)

        self.connect_button = CTkButton(self.frame1, text="Connect", font=("cairo", 14, "bold"),
                                        command=self.com_connect, fg_color="green")
        self.connect_button.pack( pady=15, padx=15)

        self.start_all_button = CTkButton(self.frame1, text="Start all", font=("cairo", 14, "bold"),
                                          command=self.startAll)
        self.start_all_button.pack(pady=15, padx=15)

        self.figure = Figure(figsize=(8, 5), dpi=110)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Operations Reading vs. Time")
        self.ax.set_ylabel("Operations reading")
        self.ax.set_xlabel("Operations time")
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame1)
        self.canvas.get_tk_widget().pack(pady=(20, 0))
        toolsbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.canvas._tkcanvas.pack()

        self.top_frame = CTkScrollableFrame(self.top, corner_radius=15, width=900, height=700)
        self.top_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        ################################## 1 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=0, column=0, pady=10, padx=10)

        self.enable1 = CTkCheckBox(self.frame3, text="enable")
        self.enable1.pack(pady=10, padx=10)

        self.display_op_name1 = CTkEntry(self.frame3, placeholder_text="Operation1",
                                        font=("roboto", 16, "bold"), width=250)
        self.display_op_name1.pack(pady=10, padx=10)

        self.display_op_time1 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                        font=("roboto", 16, "bold"), width=250)
        self.display_op_time1.pack(pady=10, padx=10)

        self.display_op_times1 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_times1.pack(pady=10, padx=10)

        self.display_op_res1 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res1.pack(pady=10, padx=10)

        self.display_op_result1 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                          wraplength=250)
        self.display_op_result1.pack(pady=(0, 10), padx=10)

        self.start_button1 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("1"))
        self.start_button1.pack(pady=10, padx=10)

        # self.stop_button1 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button1.pack(pady=10, padx=10)

        ################################## 2 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=0, column=1, pady=10, padx=10)

        self.enable2 = CTkCheckBox(self.frame3, text="enable")
        self.enable2.pack(pady=10, padx=10)

        self.display_op_name2 = CTkEntry(self.frame3, placeholder_text="Operation2",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name2.pack(pady=10, padx=10)

        self.display_op_time2 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time2.pack(pady=10, padx=10)

        self.display_op_times2 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times2.pack(pady=10, padx=10)

        self.display_op_res2 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res2.pack(pady=10, padx=10)

        self.display_op_result2 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result2.pack(pady=(0, 10), padx=10)

        self.start_button2 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("2"))
        self.start_button2.pack(pady=10, padx=10)

        # self.stop_button2 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button2.pack(pady=10, padx=10)

        ################################## 3 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=0, column=2, pady=10, padx=10)

        self.enable3 = CTkCheckBox(self.frame3, text="enable")
        self.enable3.pack(pady=10, padx=10)

        self.display_op_name3 = CTkEntry(self.frame3, placeholder_text="Operation3",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name3.pack(pady=10, padx=10)

        self.display_op_time3 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time3.pack(pady=10, padx=10)

        self.display_op_times3 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times3.pack(pady=10, padx=10)

        self.display_op_res3 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res3.pack(pady=10, padx=10)

        self.display_op_result3 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result3.pack(pady=(0, 10), padx=10)

        self.start_button3 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("3"))
        self.start_button3.pack(pady=10, padx=10)

        # self.stop_button3 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button3.pack(pady=10, padx=10)

        ################################## 4 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=1, column=0, pady=10, padx=10)

        self.enable4 = CTkCheckBox(self.frame3, text="enable")
        self.enable4.pack(pady=10, padx=10)

        self.display_op_name4 = CTkEntry(self.frame3, placeholder_text="Operation4",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name4.pack(pady=10, padx=10)

        self.display_op_time4 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time4.pack(pady=10, padx=10)

        self.display_op_times4 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times4.pack(pady=10, padx=10)

        self.display_op_res4 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res4.pack(pady=10, padx=10)

        self.display_op_result4 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result4.pack(pady=(0, 10), padx=10)

        self.start_button4 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("4"))
        self.start_button4.pack(pady=10, padx=10)

        # self.stop_button4 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button4.pack(pady=10, padx=10)

        ################################## 5 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=1, column=1, pady=10, padx=10)

        self.enable5 = CTkCheckBox(self.frame3, text="enable")
        self.enable5.pack(pady=10, padx=10)

        self.display_op_name5 = CTkEntry(self.frame3, placeholder_text="Operation5",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name5.pack(pady=10, padx=10)

        self.display_op_time5 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time5.pack(pady=10, padx=10)

        self.display_op_times5 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times5.pack(pady=10, padx=10)

        self.display_op_res5 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res5.pack(pady=10, padx=10)

        self.display_op_result5 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result5.pack(pady=(0, 10), padx=10)

        self.start_button5 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("5"))
        self.start_button5.pack(pady=10, padx=10)

        # self.stop_button5 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button5.pack(pady=10, padx=10)

        ################################## 6 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=1, column=2, pady=10, padx=10)

        self.enable6 = CTkCheckBox(self.frame3, text="enable")
        self.enable6.pack(pady=10, padx=10)

        self.display_op_name6 = CTkEntry(self.frame3, placeholder_text="Operation6",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name6.pack(pady=10, padx=10)

        self.display_op_time6 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time6.pack(pady=10, padx=10)

        self.display_op_times6 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times6.pack(pady=10, padx=10)

        self.display_op_res6 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res6.pack(pady=10, padx=10)

        self.display_op_result6 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result6.pack(pady=(0, 10), padx=10)

        self.start_button6 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("6"))
        self.start_button6.pack(pady=10, padx=10)

        # self.stop_button6 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button6.pack(pady=10, padx=10)

        ################################## 7 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=2, column=0, pady=10, padx=10)

        self.enable7 = CTkCheckBox(self.frame3, text="enable")
        self.enable7.pack(pady=10, padx=10)

        self.display_op_name7 = CTkEntry(self.frame3, placeholder_text="Operation7",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name7.pack(pady=10, padx=10)

        self.display_op_time7 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time7.pack(pady=10, padx=10)

        self.display_op_times7 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times7.pack(pady=10, padx=10)

        self.display_op_res7 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res7.pack(pady=10, padx=10)

        self.display_op_result7 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result7.pack(pady=(0, 10), padx=10)

        self.start_button7 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("7"))
        self.start_button7.pack(pady=10, padx=10)

        # self.stop_button7 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button7.pack(pady=10, padx=10)

        ################################## 8 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=2, column=1, pady=10, padx=10)

        self.enable8 = CTkCheckBox(self.frame3, text="enable")
        self.enable8.pack(pady=10, padx=10)

        self.display_op_name8 = CTkEntry(self.frame3, placeholder_text="Operation8",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name8.pack(pady=10, padx=10)

        self.display_op_time8 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time8.pack(pady=10, padx=10)

        self.display_op_times8 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times8.pack(pady=10, padx=10)

        self.display_op_res8 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res8.pack(pady=10, padx=10)

        self.display_op_result8 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result8.pack(pady=(0, 10), padx=10)

        self.start_button8 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("8"))
        self.start_button8.pack(pady=10, padx=10)

        # self.stop_button8 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button8.pack(pady=10, padx=10)

        ################################## 9 ###################################

        self.frame3 = CTkFrame(self.top_frame, corner_radius=15, fg_color="black")
        self.frame3.grid(row=2, column=2, pady=10, padx=10)

        self.enable9 = CTkCheckBox(self.frame3, text="enable")
        self.enable9.pack(pady=10, padx=10)

        self.display_op_name9 = CTkEntry(self.frame3, placeholder_text="Operation9",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_name9.pack(pady=10, padx=10)

        self.display_op_time9 = CTkEntry(self.frame3, placeholder_text="Time (sec)",
                                         font=("roboto", 16, "bold"), width=250)
        self.display_op_time9.pack(pady=10, padx=10)

        self.display_op_times9 = CTkEntry(self.frame3, placeholder_text="Scan times",
                                          font=("roboto", 16, "bold"), width=250)
        self.display_op_times9.pack(pady=10, padx=10)

        self.display_op_res9 = CTkLabel(self.frame3, text="Results", font=("roboto", 16, "bold"), width=250)
        self.display_op_res9.pack(pady=10, padx=10)

        self.display_op_result9 = CTkLabel(self.frame3, text="", font=("roboto", 13, "bold"), width=250,
                                           wraplength=250)
        self.display_op_result9.pack(pady=(0, 10), padx=10)

        self.start_button9 = CTkButton(self.frame3, text="Start", command=lambda: self.startOP("9"))
        self.start_button9.pack(pady=10, padx=10)

        # self.stop_button9 = CTkButton(self.frame3, text="Stop", fg_color="brown")
        # self.stop_button9.pack(pady=10, padx=10)

        ani = FuncAnimation(self.figure, self.animateBlot, interval=400)

        self.top.mainloop()

    def startOP(self, opnum):
        try:
            if opnum == "1":
                th1 = threading.Thread(target=self.op1)
                th1.start()
            if opnum == "2":
                th2 = threading.Thread(target=self.op2)
                th2.start()
            if opnum == "3":
                th3 = threading.Thread(target=self.op3)
                th3.start()
            if opnum == "4":
                th4 = threading.Thread(target=self.op4)
                th4.start()
            if opnum == "5":
                th5 = threading.Thread(target=self.op5)
                th5.start()
            if opnum == "6":
                th6 = threading.Thread(target=self.op6)
                th6.start()
            if opnum == "7":
                th7 = threading.Thread(target=self.op7)
                th7.start()
            if opnum == "8":
                th8 = threading.Thread(target=self.op8)
                th8.start()
            if opnum == "9":
                th9 = threading.Thread(target=self.op9)
                th9.start()
        except Exception as q:
            print("Start OP: ", q)

    def startAll(self):
        try:
            if self.enable1.get():
                th1 = threading.Thread(target=self.op1)
                th1.start()
            if self.enable2.get():
                th2 = threading.Thread(target=self.op2)
                th2.start()
            if self.enable3.get():
                th3 = threading.Thread(target=self.op3)
                th3.start()
            if self.enable4.get():
                th4 = threading.Thread(target=self.op4)
                th4.start()
            if self.enable5.get():
                th5 = threading.Thread(target=self.op5)
                th5.start()
            if self.enable6.get():
                th6 = threading.Thread(target=self.op6)
                th6.start()
            if self.enable7.get():
                th7 = threading.Thread(target=self.op7)
                th7.start()
            if self.enable8.get():
                th8 = threading.Thread(target=self.op8)
                th8.start()
            if self.enable9.get():
                th9 = threading.Thread(target=self.op9)
                th9.start()
            messagebox.showinfo("Starting!", "All enabled sections started!")
        except Exception as z:
            print("Start all: ", z)

    def op1(self):

        if self.enable1.get():
            if self.display_op_name1.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time1.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times1.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data1 = []
                xx = ""
                for i in range(int(self.display_op_times1.get())):
                    # try:
                    #     details1 = self.arduino.readline().decode().rstrip()
                    #     print(details1)
                    #     self.data1.append(details1)
                    # except AttributeError:
                    #     messagebox.showerror("Connection error!", "Connect with board first!")
                    # except:
                    #     continue
                    try:
                        self.data1.append(randint(50, 1000))
                        time.sleep(float(self.display_op_time1.get()))
                        xx += str(self.data1[i]) + ", "
                        self.display_op_result1.configure(text=xx)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except Exception as f:
                        print(f)
        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op2(self):
        if self.enable2.get():
            if self.display_op_name2.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time2.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times2.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data2 = []
                xx2 = ""
                for i in range(int(self.display_op_times2.get())):
                    # try:
                    #     details2 = float(self.arduino.readline().decode().rstrip())
                    #     self.data2.append(details2)
                    # except AttributeError:
                    #     messagebox.showerror("Connection error!", "Connect with board first!")
                    # except:
                    #     continue
                    try:
                        self.data2.append(randint(50, 1000))
                        time.sleep(float(self.display_op_time2.get()))
                        xx2 += str(self.data2[i]) + ", "
                        self.display_op_result2.configure(text=xx2)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue
        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op3(self):
        if self.enable3.get():
            if self.display_op_name3.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time3.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times3.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data3 = []
                xx3 = ""
                for i in range(int(self.display_op_times3.get())):
                    try:
                        details3 = float(self.arduino.readline().decode().rstrip())
                        self.data3.append(details3)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        # self.data3.append(randint(0, 500))
                        time.sleep(float(self.display_op_time3.get()))
                        xx3 += str(self.data3[i]) + ", "
                        self.display_op_result3.configure(text=xx3)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op4(self):
        if self.enable4.get():
            if self.display_op_name4.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time4.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times4.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data4 = []
                xx4 = ""
                for i in range(int(self.display_op_times4.get())):
                    try:
                        details4 = float(self.arduino.readline().decode().rstrip())
                        self.data4.append(details4)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time4.get()))
                        xx4 += str(self.data4[i]) + ", "
                        self.display_op_result4.configure(text=xx4)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op5(self):
        if self.enable5.get():
            if self.display_op_name5.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time5.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times5.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data5 = []
                xx5 = ""
                for i in range(int(self.display_op_times5.get())):
                    try:
                        details5 = float(self.arduino.readline().decode().rstrip())
                        self.data5.append(details5)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time5.get()))
                        xx5 += str(self.data5[i]) + ", "
                        self.display_op_result5.configure(text=xx5)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op6(self):
        if self.enable6.get():
            if self.display_op_name6.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time6.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times6.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data6 = []
                xx6 = ""
                for i in range(int(self.display_op_times6.get())):
                    try:
                        details6 = float(self.arduino.readline().decode().rstrip())
                        self.data6.append(details6)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time6.get()))
                        xx6 += str(self.data6[i]) + ", "
                        self.display_op_result6.configure(text=xx6)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op7(self):
        if self.enable7.get():
            if self.display_op_name7.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time7.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times7.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data7 = []
                xx7 = ""
                for i in range(int(self.display_op_times7.get())):
                    try:
                        details7 = float(self.arduino.readline().decode().rstrip())
                        self.data7.append(details7)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time7.get()))
                        xx7 += str(self.data7[i]) + ", "
                        self.display_op_result7.configure(text=xx7)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def op8(self):
        if self.enable8.get():
            if self.display_op_name8.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time8.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times8.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data8 = []
                xx8 = ""
                for i in range(int(self.display_op_times8.get())):
                    try:
                        details8 = float(self.arduino.readline().decode().rstrip())
                        self.data8.append(details8)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time8.get()))
                        xx8 += str(self.data1[i]) + ", "
                        self.display_op_result8.configure(text=xx8)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")


    def op9(self):
        if self.enable9.get():
            if self.display_op_name9.get() == "":
                messagebox.showerror("Name error!", "Operation name must be assigned!")
            elif float(self.display_op_time9.get()) < 0.01:
                messagebox.showerror("Timing error!", "Operation time must be '0.01' or longer!")
            elif int(self.display_op_times9.get()) < 1:
                messagebox.showerror("Counter error!", "Operation try times must be '1' or more!")
            else:
                self.data9 = []
                xx9 = ""
                for i in range(int(self.display_op_times9.get())):
                    try:
                        details9 = float(self.arduino.readline().decode().rstrip())
                        self.data9.append(details9)
                    except AttributeError:
                        messagebox.showerror("Connection error!", "Connect with board first!")
                    except:
                        continue
                    try:
                        time.sleep(float(self.display_op_time1.get()))
                        xx9 += str(self.data9[i]) + ", "
                        self.display_op_result9.configure(text=xx9)
                        self.canvas.draw()
                        plt.pause(0.0001)
                    except:
                        continue

        else:
            messagebox.showwarning("Notify!", "Enable the section !")

    def animateBlot(self, i):
        try:
            self.ax.clear()
            self.ax.set_title("Operations Reading vs. Time")
            self.ax.set_ylabel("Operations reading")
            self.ax.set_xlabel("Operations time")

            if self.enable1.get():
                self.ax.plot(self.data1, marker=".", label=self.display_op_name1.get())
            if self.enable2.get():
                self.ax.plot(self.data2, label=self.display_op_name2.get())
            if self.enable3.get():
                self.ax.plot(self.data3, marker=".", label=self.display_op_name3.get())
            if self.enable4.get():
                self.ax.plot(self.data4, label=self.display_op_name4.get())
            if self.enable5.get():
                self.ax.plot(self.data5, marker=".", label=self.display_op_name5.get())
            if self.enable6.get():
                self.ax.plot(self.data6, label=self.display_op_name6.get())
            if self.enable7.get():
                self.ax.plot(self.data7, marker=".", label=self.display_op_name7.get())
            if self.enable8.get():
                self.ax.plot(self.data8, label=self.display_op_name8.get())
            if self.enable9.get():
                self.ax.plot(self.data9, marker=".", label=self.display_op_name9.get())

            self.ax.legend(loc="upper right")
            plt.show()
        except Exception as e:
            print(e)



A().Gui()