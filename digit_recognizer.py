import customtkinter as ctk
import tkinter as tk
import PIL.ImageGrab as ImageGrab
from PIL import Image
import numpy as np
from keras.models import load_model
import math
model = load_model("my_model")


ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

class DrawApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Digit identifier")
        self.root.geometry("1040x730")

        self.pointer_size = 30
        self.background = ctk.CTkCanvas(self.root,bg='black',bd = 0,borderwidth=0,height=128 * 5,width=128 * 5)
        self.background.place(x=250,y=60)
        self.background.bind("<B1-Motion>",self.paint) 
        self.background.bind("<ButtonRelease-1>",self.predict_1) 
        self.clear_screen= ctk.CTkButton(self.root,text="Clear",command= lambda : self.background.delete('all')
        ,width=20, height=20, fg_color="transparent", font=('Arial', 40))
        self.clear_screen.place(x=20,y=180)

        # self.pred_btn = ctk.CTkButton(self.root, text='Predict', command=self.predict_2
        # ,width=20, height=20, fg_color="transparent", font=('Arial', 40))
        # self.pred_btn.place(x=20, y = 320)
        self.save_btn = ctk.CTkButton(self.root, text='Save', command=self.save_drawing
        ,width=20, height=20, fg_color="transparent", font=('Arial', 40))
        self.save_btn.place(x=20, y = 250)
        
        self.label_0 = ctk.CTkLabel(self.root, text='0 (0%)', font=('Arial', 44))
        self.output = ctk.CTkLabel(self.root, text='Predict digit:', font=('Arial', 30))
        self.output.place(x = 20, y = 460)
        self.my_slider = ctk.CTkSlider(self.root, from_=1, to=50, orientation='vertical', command=self.choose_pointer_size, width=30, height=600, number_of_steps=25)
        self.my_slider.set(30)
        self.my_slider.place(x = 950, y = 100)
        self.slider_label = ctk.CTkLabel(self.root, text=f'\N{Lower Right Pencil} {self.pointer_size}', font=('Arial', 30))
        self.slider_label.place(x = 925, y = 50)
        self.label_0.place(x = 20, y = 500)

    def choose_pointer_size(self, value):
        self.pointer_size = int(value)
        self.slider_label.configure(text=f'\N{Lower Right Pencil} {self.pointer_size}')
    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  
        self.background.create_rectangle(x1,y1,x2,y2,fill='white',outline='white',width=self.pointer_size)
    def save_drawing(self):
        try:
            x=self.root.winfo_rootx() + self.background.winfo_x()
            y=self.root.winfo_rooty() + self.background.winfo_y()
            x1= x + self.background.winfo_width() 
            y1= y + self.background.winfo_height()
            ImageGrab.grab().crop((x , y, x1, y1)).resize((28, 28)).save('image.jpg')
            # messagebox.showinfo('Screenshot Successfully Saved as' + str(file_ss))
        except:
            print("Error in saving the screenshot")

    def predict_1(self, foo):
        # image = Image.open("image.jpg").convert('L')
        x=self.root.winfo_rootx() + self.background.winfo_x()
        y=self.root.winfo_rooty() + self.background.winfo_y()
        x1= x + self.background.winfo_width() 
        y1= y + self.background.winfo_height()
        image = np.array(ImageGrab.grab().crop((x , y, x1, y1)).resize((28, 28)).convert('L'))
        image = image.reshape(1, 28,28)
        image = image / 255
        pred = model.predict(image)
        print(np.argmax(pred))
        self.label_0.configure(text = f'{np.argmax(pred)} ({math.floor(pred[0][np.argmax(pred)] * 100)}%)')

    def predict_2(self):
        # image = Image.open("image.jpg").convert('L')
        x=self.root.winfo_rootx() + self.background.winfo_x()
        y=self.root.winfo_rooty() + self.background.winfo_y()
        x1= x + self.background.winfo_width() 
        y1= y + self.background.winfo_height()
        image = np.array(ImageGrab.grab().crop((x , y, x1, y1)).resize((28, 28)).convert('L'))
        image = image.reshape(1, 28,28)
        image = image / 255
        pred = model.predict(image)
        # self.label_0.configure(text = f'{np.argmax(pred)} Hi ({list(pred)[np.argmax(pred)]})')

if __name__ =="__main__":
    root = ctk.CTk()
    p = DrawApp(root)
    root.mainloop()
    