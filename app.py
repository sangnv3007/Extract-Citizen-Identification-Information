import cv2
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from process import ReturnInfoCard
import json
import time
import sys

def uploadF():
    global pathFront
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameF = fd.askopenfilename(
        title='Chọn ảnh mặt trước CCCD',
        initialdir='/',
        filetypes=filetypes)
    imgFront = ImageTk.PhotoImage(Image.open(filenameF).resize((400, 270)))
    label_photo.configure(image=imgFront)
    label_photo.image = imgFront
    bt_uploadF.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadF.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueF.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    pathFront = filenameF


def changeForm():
    lb_title.configure(text="Chụp lại ảnh CMND/Thẻ căn cước mặt sau của bạn")
    imgBack = ImageTk.PhotoImage(Image.open('cmt_back.29611820.png'))
    label_photo.configure(image=imgBack)
    label_photo.image = imgBack
    bt_uploadF.destroy()
    bt_continueF.destroy()
    bt_uploadB.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)

def gobackFormF():
    print()
def uploadB():
    global pathBack
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameB = fd.askopenfilename(
        title='Chọn ảnh mặt sau CCCD',
        initialdir='/',
        filetypes=filetypes)
    imgBack = ImageTk.PhotoImage(Image.open(filenameB).resize((400, 270)))
    label_photo.configure(image=imgBack)
    label_photo.image = imgBack
    bt_uploadB.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadB.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueB.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    label_return.place(relx=0.5, rely=0.8, anchor=CENTER)
    pathBack = filenameB
def process():
    process_bar.place(relx=0.5, rely=0.9, anchor=CENTER)
    process_bar['value'] = 0
    process_bar['value'] = 20
    formF.update_idletasks()
    obj1 = ReturnInfoCard(pathFront)
    json_string_F = json.dumps({"errorCode": obj1.errorCode, "errorMessage": obj1.errorMessage,
                                "data":[{"id": obj1.id, "name": obj1.name, "dob": obj1.dob,"sex": obj1.sex,
                                "nationality": obj1.nationality,"home": obj1.home, "address": obj1.address,
                                "doe": obj1.doe,"imageFace": obj1.imageFace, "type": obj1.type}]},ensure_ascii=False).encode('utf8')
    print(json_string_F.decode())
    process_bar['value'] = 60
    formF.update_idletasks()
    obj2 = ReturnInfoCard(pathBack)
    process_bar['value'] = 80
    formF.update_idletasks()
    json_string_B = json.dumps({"errorCode": obj2.errorCode, "errorMessage": obj2.errorMessage,
                                "data":[{"features": obj2.features, "issue_date": obj2.issue_date,
                                "type": obj2.type}]}, ensure_ascii= False).encode('utf8')
    print(json_string_B.decode())
    process_bar['value'] = 100
    bt_continueB.destroy()
    bt_uploadB.destroy()
    process_bar.destroy()
    lb_title.configure(text="Chụp lại ảnh khuôn mặt của bạn")
    lb_notice.configure(text="")
    imgFace = ImageTk.PhotoImage(Image.open('face.c8f1db03.png'))
    label_photo.configure(image=imgFace)
    label_photo.image = imgFace
    bt_uploadFace.place(relx=0.5, rely=0.8, anchor=CENTER, width=500)

def uploadFace():
    global pathFace
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameFace = fd.askopenfilename(
        title='Chọn ảnh khuôn mặt công dân',
        initialdir='/',
        filetypes=filetypes)
    imgFace = ImageTk.PhotoImage(Image.open(filenameFace).resize((200, 350)))
    label_photo.configure(image=imgFace)
    label_photo.image = imgFace
    bt_uploadFace.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadFace.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueFace.place(relx=0.7, rely=0.8, anchor=CENTER, width=250)
    pathFace = filenameFace
    
def res():
    print("Ket qua xac minh")
    print(pathFront)
    print(pathBack)
    print(pathFace)
# Create formF
formF = Tk()
formF.title("Chương trình demo eKYC")
formF.geometry("800x600")
#
lb_title = Label(formF, text="Chụp lại ảnh CMND/Thẻ căn cước mặt trước của bạn", font='Arial 16 bold')
lb_title.pack(side="top")
#
lb_notice = Label(
    formF, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Arial 8', fg='red')
lb_notice.place(relx=0.5, rely=0.1, anchor=CENTER)
#
photoF = PhotoImage(file="cmt.be3f6567.png")
label_photo = Label(image=photoF)
label_photo.place(relx=0.5, rely=0.4, anchor=CENTER)
#
bt_uploadF = Button(formF, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadF)
bt_uploadF.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)
bt_continueF = Button(formF, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command=changeForm)
bt_continueF.place(width=0)
#
label_return = Button(formF, text="Quay lại", font=("Arial 16 bold"), bg="white", fg='red', command=gobackFormF)
bt_uploadB = Button(formF, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadB)
bt_uploadB.place(width=0)
process_bar = ttk.Progressbar(formF, orient = HORIZONTAL, length = 400, mode = 'determinate')
bt_continueB = Button(formF, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command=process)
bt_continueB.place(width=0)
#
bt_uploadFace = Button(formF, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadFace)
bt_uploadFace.place(width=0)
bt_continueFace = Button(formF, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command=res)
bt_continueFace.place(width=0)
formF.mainloop()