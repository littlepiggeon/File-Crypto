from os.path import getsize, exists
from tkinter import Tk, ttk, messagebox, filedialog


def decrypto():
    if not (exists(lab_in.cget('text')) or lab_out.cget('text')):
        messagebox.showerror('错误', '路径不存在！')
        return

    btn_start.configure(state='disable')
    btn_in.configure(state='disable')
    btn_out.configure(state='disable')
    en_key.configure(state='readonly')
    root.update()

    total = getsize(lab_in.cget('text'))
    pb.configure(maximum=total)
    key = en_key.get()

    rf = open(lab_in.cget('text'), 'rb')
    try:
        with open(lab_out.cget('text'), 'wb') as wf:
            while True:
                for char in key:
                    d = rf.read(1)
                    if not d:
                        btn_start.configure(state='enable')
                        btn_in.configure(state='enable')
                        btn_out.configure(state='enable')
                        en_key.configure(state='enable')
                        root.update()
                        messagebox.showinfo('信息', '解密完成！')
                        return
                    data = d[0]
                    while True:
                        if (data - ord(char)) < 0:
                            data = data + ord(char) + 255
                        else:
                            c = (data - ord(char)).to_bytes(1, 'big')
                            break
                    pb.step(wf.write(c))
                    lab_rate.configure(text=f'{pb.cget("value") / total:.2f}%')
                    root.update()
    except FileNotFoundError:
        messagebox.showerror('错误', '路径不存在！')


root = Tk('Decrypto')
root.title('Decrypto')

ttk.Label(root, text='输入：').grid(row=0, column=0)
lab_in = ttk.Label(root)
lab_in.grid(row=0, column=1)
lab_in.grid(row=0, column=1)
btn_in = ttk.Button(root, text='浏览',
                    command=lambda: lab_in.configure(text=filedialog.askopenfilename(defaultextension='.crypto',
                                                                                     filetypes=(
                                                                                     ('加密后的文件', '*.crypto'),))))
btn_in.grid(row=0, column=2)

ttk.Label(root, text='密码：').grid(row=1, column=0)
en_key = ttk.Entry(root, width=30)
en_key.grid(row=1, column=1)

ttk.Label(root, text='输出：').grid(row=2, column=0)
lab_out = ttk.Label(root)
lab_out.grid(row=2, column=1)
lab_out.grid(row=2, column=1)
btn_out = ttk.Button(root, text='浏览', command=lambda: lab_out.configure(
    text=filedialog.asksaveasfilename(filetypes=(('所有文件', '*'),))))
btn_out.grid(row=2, column=2)

btn_start = ttk.Button(root, text='开始', command=decrypto)
btn_start.grid(row=3, column=0, columnspan=3)

lab_rate = ttk.Label(root, text='--.--%')
lab_rate.grid(row=4, column=0)

pb = ttk.Progressbar(root, mode='determinate', length=300)
pb.grid(row=4, column=1, columnspan=2)

root.mainloop()
