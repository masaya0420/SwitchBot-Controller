import tkinter as tk; import json
import requests; import os
from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame, CTkToplevel,CTkSlider, CTkEntry, CTkTextbox # type: ignore
import customtkinter as ctk # type: ignore
import time


user_name = os.getlogin()


#tkinter
ctk.set_appearance_mode("dark")  # ダークモード
ctk.set_default_color_theme("blue")  # テーマカラー
root = ctk.CTk()
root.geometry("700x500")
last_time = 0
delay = 0.5
API_KEY = ""
devicekey = ""
device_name = ""
device_row = 1


def setup():
    #セットアップのタブを作成する
    setup_tab = CTkToplevel()
    setup_tab.title("セットアップ")
    setup_tab.geometry("300x200")
    #セットアップの入力フォームを作成する
    global API_KEY
    api_text = CTkEntry(setup_tab, width=300,placeholder_text="API KEYを入力")
    api_text.grid(row=0,column=0)
    def setup_get():
        global API_KEY
        API_KEY = api_text.get()
        setup_tab.destroy()
    api_get_button = CTkButton(setup_tab, text="保存", command=setup_get)
    api_get_button.grid(row=1, column=0)

#追加したボタン等をjson形式
def hozon_jsonConfig():
    device_data = {
        "device_name": device_name,
        "devicekey": devicekey,
        "API_KEY": API_KEY
    }
    try:
        with open("device_data.json", "r") as f:
            device_info_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # ファイルがない場合や読み込みエラー時は空リストで初期化
        device_info_list = []

    # 新しいデバイス情報をリストに追加
    device_info_list.append(device_data)
    
    # データをファイルに保存
    with open("device_data.json", "w") as f:
        json.dump(device_info_list, f, indent=2)  # インデント付きで整形


#chatBot生成 jsonファイルからconfigをロードする処理　説明のためにコメントアウトも生成させたが、眠たいため理解せず使う
def load_device_info():
    global device_row  # すでに定義されているdevice_rowを使用
    """デバイス情報を保存したJSONファイルから読み込む"""
    try:
        with open("device_data.json", "r") as file:
            # ファイルの内容をリスト形式で読み込む
            device_info_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("デバイス情報ファイルが見つからないか、形式に問題があります")
        device_info_list = []  # ファイルがない場合は空のリストを返す
    
    return device_info_list

#ここも眠たいため理解せず使用
# 保存したボタンを表示する関数
def display_saved_devices():
    devices = load_device_info()
    print("読み込んだデバイス情報:", devices)

    global device_row
    device_row = 1  # 初期化

    for device in devices:
        # 必要な情報が無ければスキップ
        if "device_name" not in device or "devicekey" not in device or "API_KEY" not in device:
            print(f"⚠️ 不完全なデバイス情報をスキップ: {device}")
            continue  # スキップして次のデバイスへ

        device_name = device["device_name"]
        devicekey = device["devicekey"]
        API_KEY = device["API_KEY"]

        controll_frame = CTkFrame(root, width=100, height=100)
        controll_frame.grid(row=device_row, column=0, pady=10, padx=3)

        url = f"https://api.switch-bot.com/v1.0/devices/{devicekey}/commands"
        headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json; charset=utf8"
        }


        off_command = {
            "command": "turnOff",
            "parameter": "default",
            "commandType": "command"
        }

        on_command = {
            "command": "turnOn",
            "parameter": "default",
            "commandType": "command"
        }

        def off_swichbot():
            r = requests.post(url, headers=headers, data=json.dumps(off_command))
            print(r.text)
            json_data = r.json()
            print(json.dumps(json_data, indent=2))

        def on_swichbot():
            r = requests.post(url, headers=headers, data=json.dumps(on_command))
            print(r.text)
            json_data = r.json()
            print(json.dumps(json_data, indent=2))

        def scaledef(value):
            global last_time
            now_time = time.time()

            if now_time - last_time < delay:  # 0.1秒経ってなければスキップ
                return

            last_time = now_time

            scale = {
                "command": "setBrightness",
                "parameter": str(int(value)),
                "commandType": "command"
            }
            now_value = value
            print(now_value)
            r = requests.post(url, headers=headers, data=json.dumps(scale))
            json_data = r.json()
            print(json.dumps(json_data, indent=2))

        def confirmation():
            global confirmation_toplevel
            confirmation_toplevel = CTkToplevel()
            confirmation_toplevel.geometry("200x100")
            label = CTkLabel(confirmation_toplevel, text="本当に削除しますか？")
            label.grid(row=0, column=0)

            def destroy_controll():
                controll_frame.destroy()
                btn.destroy()
                btn1.destroy()
                confirmation_toplevel.destroy()

            def destroy_confirmation():
                confirmation_toplevel.destroy()

            yes_btn = CTkButton(confirmation_toplevel, text="はい", width=10, height=6, command=destroy_controll)
            yes_btn.grid(row=1, column=0)
            no_btn = CTkButton(confirmation_toplevel, text="いいえ", width=10, height=6, command=destroy_confirmation)
            no_btn.grid(row=1, column=1)

        # ボタンなどウィジェット設置
        btn = CTkButton(controll_frame, text="Off", width=50, height=25, command=off_swichbot)
        btn.grid(row=1, column=0)

        btn1 = CTkButton(controll_frame, text="ON", width=50, height=25, command=on_swichbot)
        btn1.grid(row=2, column=0)

        device_name_label = CTkLabel(controll_frame, text=device_name, width=100, height=10)
        device_name_label.grid(row=0, column=0)

        scale1 = CTkSlider(controll_frame, from_=1, to=100, orientation="vertical", height=90, command=scaledef)
        scale1.grid(row=1, column=3, rowspan=2, sticky="n")

        destroy_controll_button = CTkButton(controll_frame, text="X", width=3, height=3, command=confirmation)
        destroy_controll_button.grid(row=0, column=3)

        device_row += 1




#追加を押した後の処理
def add_controll_device_light():
    global device_row
    global value
    controll_frame = CTkFrame(root,width=100,height=100,)
    controll_frame.grid(row=device_row, column=0, pady=10, padx=3)
    #APIとdeviceKeyでswitchbotにリクエストを送るコード　off_swichbot、on_swichbot関数でリクエストを送り、on-off辞書でリクエストの種類を指定
    url = "https://api.switch-bot.com/v1.0/devices/" +devicekey+ "/commands"
    headers = {
    "Authorization": API_KEY,
    "Content-Type" : "application/json; charset=utf8"
    }

    off = {
    "command": "turnOff",
    "parameter": "default",
    "commandType": "command"
    }
    on = {
    "command": "turnOn",
    "parameter": "default",
    "commandType": "command"
    }
    #明るさ調整のつまみでリクエストを送る関数
    def scaledef(value):
        global last_time
        now_time = time.time()

        if now_time - last_time < delay:  # 0.1秒経ってなければスキップ
            return
    
        last_time = now_time  # ★リクエストを送る前に「今の時間」を記録！

        scale = {
            "command": "setBrightness",
            "parameter": str(int(value)),
            "commandType": "command",
        }
        now_value = value
        print(now_value)
        r = requests.post(url, headers=headers, data=json.dumps(scale))
        json_data = r.json()
        print(json.dumps(json_data, indent=2))

    def off_swichbot():
        r = requests.post(url, headers=headers, data=json.dumps(off))
        print(r.text)
        json_data = r.json()
        print(json.dumps(json_data, indent=2))

    def on_swichbot():
        r = requests.post(url, headers=headers, data=json.dumps(on))
        print(r.text)
        json_data = r.json()
        print(json.dumps(json_data, indent=2))
    #操作パネルの削除を再確認する関数
    def confirmation():
        global confirmation_toplevel
        confirmation_toplevel = CTkToplevel()
        confirmation_toplevel.geometry("200x100")
        label = CTkLabel(confirmation_toplevel, text="本当に削除しますか？")
        label.grid(row=0, column=0)

        def destroy_controll():
            controll_frame.destroy()
            btn.destroy()
            btn1.destroy()
            confirmation_toplevel.destroy()

        def destroy_confirmation():
            confirmation_toplevel.destroy()
        yes_btn = CTkButton(confirmation_toplevel, text="はい", width=10, height=6, command=destroy_controll)
        yes_btn.grid(row=1, column=0)
        no_btn= CTkButton(confirmation_toplevel, text="いいえ", width=10, height=6, command=destroy_confirmation)
        no_btn.grid(row=1, column=1)

    #デバイスのコントロールウィジェットを追加
    btn=CTkButton(controll_frame, text="Off", width=50, height=25, command=off_swichbot)
    btn.grid(row=1,column=0)
    btn1=CTkButton(controll_frame, text="ON", width=50, height=25, command=on_swichbot)
    btn1.grid(row=2,column=0)
    device_name_label = CTkLabel(controll_frame, text=device_name, width=100, height=10)
    device_name_label.grid(row=0, column=0)
    scale1=CTkSlider(controll_frame,from_=1, to=100, orientation="vertical", height=90, command=scaledef)
    scale1.grid(row=1,column=3, rowspan=2, sticky="n")
    destroy_controll_button = CTkButton(controll_frame, text="X", width=3, height=3, command=confirmation)
    destroy_controll_button.grid(row=0, column=3)


    device_row += 1

#デバイス追加のtoplevel 
def add_device_window():
    newwindow = CTkToplevel()
    newwindow.title("新しいデバイスを追加する")
    newwindow.geometry("300x200")

    name_text = CTkEntry(newwindow, width=300, placeholder_text="デバイスの名前を入力(英数字2文字以下推奨)")
    name_text.grid(row=0,column=0)
    
    deviceID = CTkEntry(newwindow, width=300, placeholder_text="deviceID(BLE MAC :を含まない)を入力")
    deviceID.grid(row=1,column=0)

    devicelist = tk.Listbox(newwindow, height=1)
    item = ["スマート電球"]
    for i in item:
        devicelist.insert(tk.END, i)
    devicelist.grid(row=2, column=0)

    def data_get():
        global devicekey
        global device_name
        device_name = name_text.get()
        devicekey = deviceID.get()
        device = devicelist.get(tk.ACTIVE)
        #deviceがitemlistと等しい場合はこの関数を実行する
        if device == "スマート電球":
            add_controll_device_light()
        newwindow.destroy()
    add_button_level = CTkButton(newwindow, text="追加", command=data_get)
    add_button_level.grid(row=3,column=0)
#使い方のtoplevel
def HowToUse():
    HowToUse_level = CTkToplevel()
    HowToUse_level.title("使い方")
    HowToUse_level.geometry("800x500")

    scrollable_frame = ctk.CTkScrollableFrame(HowToUse_level, width=700, height=950)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    HowToUse_text1 = """
        🌟 このソフトの使い方
    """
    HowToUse_text1_1 = """
        1. 最初にすること
        「セットアップ」ボタンを押して、APIキーを入力し、「保存」をクリック。
        APIキーは必ず入力してください。入力していなければ動作しません。
        また、APIキーは絶対に他人に教えないでください。悪用されると他人に部屋の電気をつけたり、消したりされます。
    """
    api_how_to_get = """
        +APIキーの取得方法
          1.スマホ版SwitchBotアプリを開く。
          2.プロフィールを開き、設定を開く。
          3.基本データを開き、アプリバージョンを10回ほどタップする。
          4.開発者向けオプションという項目が追加されるので、それを開き、トークンをAPIキーのところに入力する(長いのでコピペ推奨)
        """
    HowToUse_text2 = """
        2. デバイス（電球）を登録する
        """
    HowToUse_text2_2 = """
        「＋」ボタンでデバイス名とDeviceIDを入力。(デバイス名はなんでも良い)
        デバイスIDはAPIキーと違い、公開しても危険性は少ないですが、する必要もないので教えないでください
        デバイスIDの取得方法
        """
    deviceID_how_to_get = """
          1.追加したいデバイスの設定を開く
          2.デバイス情報を開く
          3.BLE MACをメモする(例D1:8C:7B:4F:09:5A)
          4.D1:8C:7B:4F:09:5Aの:←この文字を取り除いて、DeviceIDに入力
        """
    HowToUse_text3 = """
        3. デバイス操作
        """
    HowToUse3_3 = """
        「ON」や「OFF」を押して電球をコントロール、スライダーで明るさを調整。
    """
    HowToUse4 = """
        4. 設定の保存とロード
        """
    HowToUse4_4 = """
        デバイスなど追加した場合は必ず、保存をクリックしてください。
        ロードは基本自動で行ってくれますが、もし動作しなかった場合は手動でクリックしてください。
        
        保存したデバイス情報はjson形式でC:user:user:SwichBot.jsonもしくはzip
        に保存されているはずです。

        """
    Caution = """
        ⚠️ 注意：インターネットが必要です。
        追加してほしい機能や、エラー、わからないことがあれば気軽にDiscord .masaya. まで連絡ください。
        製作者が電球以外を持っていないためその他のデバイスは現在サポートしておりません。

        連絡いただければデバイス追加は可能ですが、デバック(バグの修正やきちんと動作するかの確認作業)
        が難しいため、暇な方はデバックに協力していただけると助かります。
        
        このソフトでは、SwitchBotのサーバーにリクエストを送り、デバイスを操作しています。
        *このソフトでは使用者の情報など一切取得しておりません。
         また、ソースコードは公開済み＆デコンパイル可能なので、ご自由に変更等していただいて構いません。
         Python初心者が頑張って作ったので、可読性等のクレームは受け付けません。
         *1.にも記載していますが、APIキー(トークン)は絶対に他人には教えないでください。
        """
        


        
    HowToUse_label1 = CTkLabel(scrollable_frame, text=HowToUse_text1, font=(None, 20))
    HowToUse_label1.grid(row=0, column=0)

    HowToUse_label1_1 = CTkLabel(scrollable_frame, text=HowToUse_text1_1)
    HowToUse_label1_1.grid(row=1, column=0)

    HowToUse_label1_2 = CTkLabel(scrollable_frame, text=api_how_to_get, text_color="red")
    HowToUse_label1_2.grid(row=2, column=0)

    HowToUse_label2 = CTkLabel(scrollable_frame, text=HowToUse_text2, font=(None, 20))
    HowToUse_label2.grid(row=3, column=0)

    HowToUse_label2_1 = CTkLabel(scrollable_frame, text=HowToUse_text2_2)
    HowToUse_label2_1.grid(row=4, column=0)

    HowToUse_label2_2 = CTkLabel(scrollable_frame, text=deviceID_how_to_get, text_color="red")
    HowToUse_label2_2.grid(row=5, column=0)

    HowToUse_label3 = CTkLabel(scrollable_frame, text=HowToUse_text3, font=(None, 20))
    HowToUse_label3.grid(row=6, column=0)
    
    HowToUse_label3_1 = CTkLabel(scrollable_frame, text=HowToUse3_3)
    HowToUse_label3_1.grid(row=7, column=0)

    HowToUse_label4 = CTkLabel(scrollable_frame, text=HowToUse4, font=(None, 20))
    HowToUse_label4.grid(row=8, column=0)

    HowToUse_label4_1 = CTkLabel(scrollable_frame, text=HowToUse4_4)
    HowToUse_label4_1.grid(row=9, column=0)

    Caution_label = CTkLabel(scrollable_frame, text=Caution)
    Caution_label.grid(row=10, column=0)



#wighet tkinter
controll_frame = CTkFrame(root, )
controll_frame.grid(row=0, column=0, sticky="ew")
addbutton = CTkButton(controll_frame, text="＋",  command=add_device_window)
addbutton.grid(row=0,column=0)
helpbutton = CTkButton(controll_frame, text="使い方",command=HowToUse)
helpbutton.grid(row=0, column=1)
setup_button = CTkButton(controll_frame, text="セットアップ" ,command=setup)
setup_button.grid(row=0, column=2)
config_save_button = CTkButton(controll_frame, text="セーブ", command=hozon_jsonConfig)
config_save_button.grid(row=0, column=3)
config_load_button = CTkButton(controll_frame, text="ロード",  command=display_saved_devices)
config_load_button.grid(row=0, column=4)



display_saved_devices()

root.mainloop()