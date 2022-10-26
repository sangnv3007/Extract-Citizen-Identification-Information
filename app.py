from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from process import ReturnInfoCard
import json

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
    lb_photo_page1.configure(image=imgFront)
    lb_photo_page1.image = imgFront
    bt_uploadF.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadF.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueF.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    pathFront = filenameF

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
    lb_photo_page2.configure(image=imgBack)
    lb_photo_page2.image = imgBack
    bt_uploadB.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadB.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueB.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    label_return_page1.place(relx=0.5, rely=0.8, anchor=CENTER)
    pathBack = filenameB

def process():
    process_bar.place(relx=0.5, rely=0.95, anchor=CENTER)
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
    process_bar.destroy()
    show_frame(page3)

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
    label_photo_page3.configure(image=imgFace)
    label_photo_page3.image = imgFace
    bt_uploadFace.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadFace.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueFace.place(relx=0.7, rely=0.8, anchor=CENTER, width=250)
    label_return_page2.place(relx=0.5, rely=0.9, anchor=CENTER)
    pathFace = filenameFace

def show_frame(frame):
    frame.tkraise()
# Create formFp
formF = Tk()
formF.title("Chương trình demo eKYC")
formF.geometry("900x700")
formF.rowconfigure(0, weight=1)
formF.columnconfigure(0, weight=1)
#formF.state('zoomed')
#setup page app
page1 = Frame(formF)
page2 = Frame(formF)
page3 = Frame(formF)
page4 = Frame(formF)
for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew') 
show_frame(page4)
# ======== Page 1(Upload front photo) ========
lb_title_page1 = Label(page1, text="Chụp lại ảnh Thẻ căn cước mặt trước của bạn", font='Arial 16 bold')
lb_title_page1.pack(side="top")
lb_notice_page1 = Label(
    page1, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Arial 8', fg='red')
lb_notice_page1.place(relx=0.5, rely=0.1, anchor=CENTER)
photoF = PhotoImage(file="cmt.be3f6567.png")
lb_photo_page1 = Label(page1, image=photoF)
lb_photo_page1.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadF = Button(page1, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadF)
bt_uploadF.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)
bt_continueF = Button(page1, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command=lambda: show_frame(page2))
bt_continueF.place(width=0)
# ======== Page 2(Upload back photo) ========
lb_title_page2 = Label(page2, text="Chụp lại ảnh Thẻ căn cước mặt sau của bạn", font='Arial 16 bold')
lb_title_page2.pack(side="top")
lb_notice_page2 = Label(
    page2, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Arial 8', fg='red')
lb_notice_page2.place(relx=0.5, rely=0.1, anchor=CENTER)
photoB = PhotoImage( file="cmt_back.29611820.png")
lb_photo_page2 = Label(page2, image=photoB)
lb_photo_page2.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadB = Button(page2, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadB)
bt_uploadB.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)
bt_continueB = Button(page2, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command= process)
bt_continueB.place(width=0)
label_return_page1 = Button(page2, text="Quay lại", font=("Arial 16 bold"), bg="white", fg='red', command=lambda: show_frame(page1))
process_bar = ttk.Progressbar(page2, orient = HORIZONTAL, length = 400, mode = 'determinate')
# ======== Page 3(Upload Face photo) ========
lb_title_page3 = Label(page3, text="Chụp lại ảnh khuôn mặt của bạn", font='Arial 16 bold')
lb_title_page3.pack(side="top")
lb_notice_page3 = Label(
    page3, text="* Vui lòng sử dụng ảnh khuôn mặt thật của bạn. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, có thể nhìn rõ khuôn mặt.",
    font='Arial 8', fg='red')
lb_notice_page2.place(relx=0.5, rely=0.1, anchor=CENTER)
imgFace = PhotoImage(file="face.c8f1db03.png")
label_photo_page3= Label(page3,image=imgFace)
label_photo_page3.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadFace = Button(page3, text="Tải ảnh/ Chụp ảnh", font=("Arial 16 bold"), bg="blue", fg='white', command=uploadFace)
bt_uploadFace.place(relx=0.5, rely=0.8, anchor=CENTER, width=600)
bt_continueFace = Button(page3, text="Tiếp theo", font=("Arial 16 bold"), bg="blue", fg='white', command=lambda: show_frame(page4))
bt_continueFace.place(width=0)
label_return_page2 = Button(page3, text="Quay lại", font=("Arial 16 bold"), bg="white", fg='red', command=lambda: show_frame(page2))

# ======== Page 4(Return result) ========
lb_title_page4 = Label(page4, text="Kết quả xác minh", font='Arial 16 bold')
lb_title_page4.pack(side="top")
#res_photo_front = PhotoImage(Image.open("CMND (480).jpeg").resize((250, 200)))
res_photo_front = ImageTk.PhotoImage(Image.open("CMND (480).jpeg").resize((200, 250)))
lb_res_front= Label(page4,image=res_photo_front)
lb_res_front.place(relx=0.2, rely=0.4, anchor=LEFT)
formF.mainloop()