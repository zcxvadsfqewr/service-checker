import customtkinter as ctk
import service_check as sck
import requests
import time
import os
import sys
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Service Checker")
app.geometry("500x300")
app.resizable(False, False)
if getattr(sys, 'frozen', False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(current_dir, "checkerlogo.ico")
app.iconbitmap(icon_path)

#таблички текст
label = ctk.CTkLabel(app, text="Состояние сервисов: ", font=("Arial", 16))
label.place(x=10, y=10)
labelcustomserv = ctk.CTkLabel(app, text= "Проверка своего сервиса: ", font=("Arial", 16))
labelcustomserv.place(x=300, y=10)

#Ввод пользователем
user_custom = ctk.CTkEntry(app)
user_custom.place(x=300, y=100)

userlabel = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
userlabel.place(x=300, y=150)
#сервисы таблички
labeldiscord = ctk.CTkLabel(app, text="Discord: ", font=("Arial", 12))
labeldiscord.place(x=10, y=60)
labelyoutube = ctk.CTkLabel(app, text="Youtube: ", font=("Arial", 12))
labelyoutube.place(x=10, y=80)
labelgithub = ctk.CTkLabel(app, text="GitHub: ", font=("Arial", 12))
labelgithub.place(x=10, y=100)
labelclaude = ctk.CTkLabel(app, text="Claude: ", font=("Arial", 12))
labelclaude.place(x=10, y=120)
labeltelegram = ctk.CTkLabel(app, text="Telegram: ", font=("Arial", 12))
labeltelegram.place(x=10, y=140)

#Таблички состояния сервисов
labelservdisc = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
labelservdisc.place(x=90, y=60)
labelservyou = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
labelservyou.place(x=90, y=80)
labelservgit = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
labelservgit.place(x=90, y=100)
labelservcld = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
labelservcld.place(x=90, y=120)
labelservtel = ctk.CTkLabel(app, text="UNKNOWN", font=("Arial", 12))
labelservtel.place(x=90, y=140)

#Привязка текста и наименований сервисов
labels_dict = {
        "discord": labelservdisc,
        "youtube": labelservyou,
        "github": labelservgit,
        "claude": labelservcld,
        "telegram": labelservtel,
    }


#кнопки
check_btn = ctk.CTkButton(app, text="Проверить", command=lambda: updatestatus())
check_btn.place(x=40, y=220)
check_btnuser = ctk.CTkButton(app, text="Проверить", command=lambda: checkuser())
check_btnuser.place(x=300, y=220)
#состояние сервисов
def updatestatus():
    check_btn.configure(text="Проверка...", state= "disabled")
    app.update()
    result = sck.serviceget()
    for name, data in result.items():
        if name in labels_dict:
            status = data["status"]

            if status == 200:
                labels_dict[name].configure(text="Работает", text_color="green")
            elif status == 403:
                labels_dict[name].configure(text="Работает но нет доступа", text_color="red")
            elif status == "connection error":
                labels_dict[name].configure(text=f"{status}", text_color= "orange")
    check_btn.configure(text="Проверить", state="normal")

#функция своей проверки
def checkuser():
    url = user_custom.get().strip()
    if not url:
        userlabel.configure(text="Введите URL", text_color="orange")
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    check_btnuser.configure(text="Проверка...", state="disabled")
    app.update()
    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )
        status = response.status_code
        if status == 200:
            userlabel.configure(text="Работает", text_color="green")
        elif status == 403:
            userlabel.configure(text="Работает но нет доступа", text_color="red")
    except requests.exceptions.ConnectionError:
        userlabel.configure(text="connection error", text_color="orange")
    check_btnuser.configure(text="Проверить", state="normal")




app.mainloop()