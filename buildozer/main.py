# main.py

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from math import *


class TextInputApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=15, padding=10)
        self.text=TextInput(font_size=50) # font_size输入文本框大小
        self.out_text=TextInput(font_size=50)
        button = Button(text="Run", size_hint=(0.5, 0.5), 
                        pos_hint={"center_x":0.5, "center_y":0.5})
        button.bind(on_press=self.press)
        layout.add_widget(self.text)
        layout.add_widget(self.out_text)
        layout.add_widget(button)
        return layout
    def press(self, instance):
        # pop = Popup(text=self.text.text)
        try: # 捕获异常，避免程序中断
            print (eval(self.text.text)) # eval内置函数，执行字符串指令
            self.out_text.text=str(eval(self.text.text))
        except:
            self.out_text.text="wrong input" # 如果是不合法信息，输出错误
            pass

if __name__=="__main__":
    TextInputApp().run()
