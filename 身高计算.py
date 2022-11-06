# -*- coding;utf-8 -*-
"""
File name : 身高计算.PY
Program IDE : PyCharm
Create file time: 2022/11/5 19:15
File Create By Author : 小梦
"""
import time
import tkinter as tk
import tkinter.ttk
from tkinter import messagebox
import progressbar
# p = progressbar.ProgressBar()
# # # 假设需要执行100个任务，放到ProgressBar()中
# for i in p(range(100)):
#     """
#     代码
#     """
#     # 假设这代码部分需要0.05s
#     time.sleep(0.05)
def run():
    name = entry.get()
    if name == '':
        messagebox.showerror("参数错误","请输入您的身高")
        return "请输入您的身高"
    if 0 < int(name) and int(name) > 250:
        messagebox.showerror("参数错误", "输入有误，请重新输入")
        return "请重新输入"
    else:
        entry.pack(padx=400)
        lable.pack(padx=400)
        progressbarOne = tkinter.ttk.Progressbar(root,length=260)
        progressbarOne.pack()
        # 进度值最大值
        progressbarOne['maximum'] = 100
        list = ["正在开启AI智能运算……","计算加密中","答案就是","就是……","正在解密","您的身高是……"]
        le = len(list)
        t = 100/le
        y = 0
        for i in range(0,7):
            text.delete(0,tk.END)
            text.insert(5,str(list[i-1]))
            text.update()
            time.sleep(0.27)
            # 进度值初始值
            y += t
            progressbarOne['value'] = y
        progressbarOne.pack(padx=400)

        text.delete(0, tk.END)
        text.insert(5, "身高是："+str(int(name)/100)+"m")
        text.update()
        time.sleep(10)
        ll = ["还在……","这点个子还不死心？","好吧","告诉你吧，我是---","小学生"]
        p = 0
        for i in ll:
            p +=1
            text.delete(0, tk.END)
            text.insert(0, i)
            text.update()
            time.sleep(1.5*p)




root = tk.Tk()      #创建一个主窗口
root.title("高级身高计算器")
root.geometry("270x110")    #窗口大小
root.resizable(0,0)
root.config(background="#fff")

lable = tk.Label(root,text="请输入您的身高(cm)：")
lable.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root,text="开始计算",command=run)
button.pack()
text = tk.Entry(root,width=20,font=('华文楷体', '12', 'bold italic'),background="#fff",borderwidth=0)
text.pack()



root.mainloop()





