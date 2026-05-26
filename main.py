import tkinter as tk
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet50
import pandas as pd
import traceback
from functions import tag
from functions import image
from resnet import main as resmain
from PIL import ImageTk

# 初始化模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = resmain.ResNet50(img_channel=3, num_classes=2).to(device)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("resnet50_model.pth", map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


# tkinter GUI
win = tk.Tk()
win.title("釣魚網站偵測")
win.geometry("500x500")
img_label = tk.Label(win)
img_label.place(x=150, y=350, width=200, height=100)

def analyze():
    url = en.get()
    if not url:
        label2.config(text="請輸入網址")
        return
    try:
        # 特徵提取
        feature = tag.tagfunc(url)
        # 轉成圖片
        img = image.genimage(feature[0])

        preview_img = img.resize((100, 100)) 
        tk_img = ImageTk.PhotoImage(preview_img)
    
        # 更新 Label圖片
        img_label.config(image=tk_img)
        img_label.image = tk_img

        # 預測
        image_tensor = transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(image_tensor)
            pred = torch.argmax(output, dim=1).item()
        result_label = "釣魚網站" if pred == 1 else "安全網站"
        label2.config(text=result_label)
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        label2.config(text=f"錯誤：{str(e)}")

# 標籤
label = tk.Label(win, bg="gray", fg="white", text="請輸入網址")
label.place(x=190, y=150, width=120, height=40)

label2 = tk.Label(win, bg=win.cget("bg"),anchor="center",  fg="black", text="結果顯示區")
label2.place(x=190, y=300, width=120, height=40)

# 輸入框
en = tk.Entry(win)
en.place(x=100, y=200, width=300, height=40)

# 按鈕
button = tk.Button(win, text="分析", command=analyze, bg="skyblue")
button.place(x=210, y=250, width=80, height=40)

win.mainloop()
