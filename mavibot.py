import cv2
import pytesseract
from PIL import ImageGrab
import pyautogui
import time
import numpy as np
import tkinter as tk
from tkinter import messagebox
import win32gui
import threading

# Tesseract'ın sistemdeki yolunu belirt (Windows için)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Belirli bir bölgenin ekran görüntüsünü al
def ekran_goruntusu_al(bolge):
    ekran = ImageGrab.grab(bbox=bolge)  # Belirli bölgeden ekran görüntüsü al
    return ekran

# Görüntüden metin tespit et (OCR)
def metin_tespit_et(image):
    # Görüntüyü OpenCV formatına çevir
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Metni çıkar
    metin = pytesseract.image_to_string(open_cv_image)
    return metin

# Pencereyi hwnd ile aktive et ve tıklama yap
def click_on_window(hwnd, x, y):
    if hwnd:
        bring_window_to_front(hwnd)
        
        # Pencerenin konumunu ve boyutlarını al
        rect = win32gui.GetWindowRect(hwnd)
        window_x, window_y = rect[0], rect[1]
        
        # Koordinatları ekran koordinatlarına dönüştür
        screen_x = x + window_x
        screen_y = y + window_y
        
        # Mouse'u belirlenen konuma taşı ve tıkla
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.click()
    else:
        print("Pencere etkinleştirilemedi.")

# Pencereyi ön plana getirmek için fonksiyon
def bring_window_to_front(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"Pencereyi ön plana getirme hatası: {e}")

# Pencere başlığına göre hwnd'yi bul
def get_window_handle_by_title(title):
    def callback(hwnd, titles):
        if win32gui.GetWindowText(hwnd) == title:
            titles.append(hwnd)
    titles = []
    win32gui.EnumWindows(callback, titles)
    return titles[0] if titles else None

# Sürekli ekran görüntüsü alıp "Çeviklik +200" olup olmadığını kontrol eden ana fonksiyon
def basla_otomatik_tiklama(bolge, hwnd):
    while app_running:
        # Ekran görüntüsünü al
        ekran_goruntusu = ekran_goruntusu_al(bolge)
        # Metni tespit et
        metin = metin_tespit_et(ekran_goruntusu)
        
        print("Bulunan metin:", metin)

        # Eğer "Çeviklik +200" metni bulunduysa, işlemi sonlandır
        if "Cvk +200" in metin or any(int(s) >= 200 for s in metin.split() if s.isdigit()):
            print("Çeviklik +200 bulundu, işlemi sonlandırıyorum.")
            break
        
        # Aksi takdirde otomatik tıklama yap
        click_on_window(hwnd, 128, 742)  # Tıklama yapılacak koordinatlar (güncelle)
        
        # Bir süre bekle (oyunun tıklamaya tepki vermesi için)
        time.sleep(5)

def start():
    global app_running
    app_running = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    messagebox.showinfo("Başlatıldı", "Otomatik tıklama başladı.")

    # Pencere hwnd'sini buraya girin
    title = "³É¼ªË¼º¹II 2.1.09.69 Pegasus -Kanal 1 À¥ÂØÍõ¹ú"
    hwnd = get_window_handle_by_title(title)
    bolge = (43, 583, 323, 670)  # Bu değerleri ekran görüntüsüne göre güncelle
    
    if hwnd:
        t = threading.Thread(target=basla_otomatik_tiklama, args=(bolge, hwnd))
        t.start()
    else:
        messagebox.showerror("Hata", "Pencere bulunamadı.")

def stop():
    global app_running
    app_running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Durduruldu", "Otomatik tıklama durduruldu.")

# Tkinter GUI'yi oluştur
app_running = False
root = tk.Tk()
root.title("Otomatik Tıklama")

start_button = tk.Button(root, text="Başla", command=start)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Durdur", command=stop, state=tk.DISABLED)
stop_button.pack(pady=10)

root.mainloop()
