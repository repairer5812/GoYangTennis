import tkinter as tk
from tkinter import Entry, messagebox
from tkinter.messagebox import askokcancel
from GoyangNaverReserVHelper import court,days,timeDicWeekdays, timeDicWeekend, timeDic, courtSearching, reservHelper

class mainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('고양시 테니스 코트 도우미')
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Label(self, text="메뉴를 선택해주세요.", font=('Helvetica', 15, "bold")).pack(side="top", padx=5, pady=5)
        # tk.Button(self, text="코트 검색하기",font=('Helvetica', 12, "bold"), width=20, height=5,
        #           command=lambda: master.switch_frame(PageOne)).pack(side="left", padx=5, pady=5)
        # tk.Button(self, text="코트 예약하기",font=('Helvetica', 12, "bold"), width=20, height=5,
        #           command=lambda: master.switch_frame(PageTwo)).pack(side="right", padx=5, pady=5)
        tk.LabelFrame(self, text="메뉴 선택", font=('Helvetica', 15, "bold"), padx=15, pady=15)
        self.grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self, text="코트 검색하기",font=('Helvetica', 12, "bold"), width=20, height=5,
                  command=lambda: master.switch_frame(PageOne)).grid(row=0, column=0, pady=10, padx=10, sticky="nswe")
        tk.Button(self, text="코트 예약하기",font=('Helvetica', 12, "bold"), width=20, height=5,
                  command=lambda: master.switch_frame(PageTwo)).grid(row=0, column=1, pady=10, padx=10, sticky="nswe")      

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self, text="검색할 코트와 조건을 설정해주세요.", font=('Helvetica', 15, "bold")).grid(row=1, column=0, pady=10, padx=10, columnspan=4)
        tk.Button(self, text="뒤로 돌아가기",font=('Helvetica', 12),
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=7, pady=10, padx=10)
        tk.Label(self, text="코트", font=('Helvetica', 12, "bold")).grid(row=2, column=0, pady=10, padx=10)
        for i in range(1,7):
            court[i][1] = tk.BooleanVar()
            tk.Checkbutton(self,text="{0}".format(court[i][0]),font=('Helvetica', 12, "bold"), variable=court[i][1]).grid(row=2,column=i,padx=10)
        
        tk.Label(self, text="주중", font=('Helvetica', 12, "bold")).grid(row=3, column=0, pady=10, padx=10)
        for k in range(1,6):
            days[k][1] = tk.BooleanVar()
            tk.Checkbutton(self,text="{0}".format(days[k][0]),font=('Helvetica', 12, "bold"), variable=days[k][1]).grid(row=3,column=k,padx=10)

        tk.Label(self, text="주중 시간", font=('Helvetica', 12, "bold")).grid(row=4, column=0, pady=10, padx=10)
        for k in range(1,9):
            timeDicWeekdays[k][1] = tk.BooleanVar()
            tk.Checkbutton(self,text="{0}".format(timeDicWeekdays[k][0]),font=('Helvetica', 12, "bold"), variable=timeDicWeekdays[k][1]).grid(row=4,column=k,padx=10)

        tk.Label(self, text="주말", font=('Helvetica', 12, "bold")).grid(row=5, column=0, pady=10, padx=10)
        for k in range(6,8):
            days[k][1] = tk.BooleanVar()
            tk.Checkbutton(self,text="{0}".format(days[k][0]),font=('Helvetica', 12, "bold"), variable=days[k][1]).grid(row=5,column=k-5,padx=10)

        tk.Label(self, text="주말 시간", font=('Helvetica', 12, "bold")).grid(row=6, column=0, pady=10, padx=10)
        for k in range(1,9):
            timeDicWeekend[k][1] = tk.BooleanVar()
            tk.Checkbutton(self,text="{0}".format(timeDicWeekend[k][0]),font=('Helvetica', 12, "bold"), variable=timeDicWeekend[k][1]).grid(row=6,column=k,padx=10)
        
        # notHeadless = tk.BooleanVar()
        # tk.Checkbutton(self,text="검색 과정 보기",font=('Helvetica', 12, "bold"), variable = notHeadless).grid(row=7,column=3,padx=10)
        tk.Button(self, text="코트 검색 시작하기",font=('Helvetica', 15, "bold"),
                  command=CommandConditionCheck1).grid(row=7, column=4, pady=10, padx=10, columnspan=4)

def CommandConditionCheck1():
    # 코트 점검
    # 요일 점검
    # 주중, 주말 시간 점검
    courtSum = 0
    WeekdaysSum = 0
    WeekendSum = 0
    daysSum = 0
    timeDicWeekdaysSum = 0
    timeDicWeekendSum = 0
    commandCounter = 0
    for i in range(1,7):
        courtSum += court[i][1].get()
    if courtSum == 0:
        messagebox.showerror("Error", "코트를 선택하지 않으셨습니다.")
    else:
        commandCounter += 1

    for j in range(1,8):
        if j < 6:
            WeekdaysSum += days[j][1].get()
        elif j >=6:
            WeekendSum += days[j][1].get()    
    daysSum = WeekdaysSum + WeekendSum
    if daysSum == 0:
        messagebox.showerror("Error", "요일을 선택하지 않으셨습니다.")
    else:
        commandCounter += 1


    if WeekdaysSum > 0:
        for k in range(1,9):
            timeDicWeekdaysSum += timeDicWeekdays[k][1].get() 
        if timeDicWeekdaysSum == 0:
            messagebox.showerror("Error", "주중 시간을 선택하지 않으셨습니다.")
        else:
            commandCounter += 1    
    else:
        commandCounter += 1

    if WeekendSum > 0:
        for k in range(1,9):
            timeDicWeekendSum += timeDicWeekend[k][1].get() 
        if timeDicWeekendSum == 0:
            messagebox.showerror("Error", "주말 시간을 선택하지 않으셨습니다.")
        else:
            commandCounter += 1
    else:
        commandCounter += 1
    
    if commandCounter == 4:
        # messagebox.showerror("Error", "아직 개발중입니다.")
        courtSearching()
        

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self, text="F8 시간 선택 F9 예약정보 F10 결제 F4 처음페이지", font=('Helvetica', 15, "bold")).grid(row=1, column=0, pady=10, padx=10, columnspan=6)
        tk.Button(self, text="뒤로 돌아가기",font=('Helvetica', 12),
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=7, pady=10, padx=10, columnspan=2)
        
        courtValue = tk.IntVar()
        tk.Label(self, text="코트", font=('Helvetica', 12, "bold")).grid(row=2, column=0, pady=10, padx=10)
        for i in range(1,7):
            tk.Radiobutton(self, text = "{0}".format(court[i][0]), font=('Helvetica', 12, "bold"), value = i, variable= courtValue).grid(row=2,column=i, padx=10)
                    
        timeValue = tk.IntVar()
        tk.Label(self, text="예약 시간", font=('Helvetica', 12, "bold")).grid(row=3, column=0, pady=10, padx=10)
        for k in range(1,9):
            tk.Radiobutton(self, text="{0}".format(timeDic[k][0]), font=('Helvetica', 12, "bold"), value = k, variable=timeValue).grid(row=3,column=k,padx=10)
        
        address = Entry(self, width=30,font=('Helvetica', 12, "bold"))
        address.grid(row=4,column=0, columnspan=8)
        address.insert(0,"고양시, 일산서구, 덕이동")
        tk.Button(self, text="코트 예약 시작하기",font=('Helvetica', 15, "bold"),
                  command=lambda: CommandConditionCheck2(courtValue,timeValue,address)).grid(row=7, column=0, pady=10, padx=10, columnspan=8)

def CommandConditionCheck2(courtValue,timeValue,address):
    if courtValue.get() == 0:
        messagebox.showerror("Error", "코트를 선택하지 않으셨습니다.")
    elif timeValue.get() == 0:
        messagebox.showerror("Error", "시간을 선택하지 않으셨습니다.")
    else:
        confirm(courtValue.get(),timeValue.get(),address.get())
        

def confirm(courtValue,timeValue,address):
    answer = askokcancel(title='확인',
                    message=' 코트: {0}\n 예약시간: {1} \n 주소: {2} \n 진행할까요?'.format(court[courtValue][0],timeDic[timeValue][0],address))
    if answer:
        reservHelper(courtValue,timeValue,address)

app = mainApp()
app.mainloop()