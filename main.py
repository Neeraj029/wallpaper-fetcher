import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GdkPixbuf

class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")
        self.set_default_size(200, 200)
        self.set_border_width(10)

        self.header = Gtk.HeaderBar()
        self.header.props.show_close_button = True

        self.set_titlebar(self.header)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Search")
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "edit-find-symbolic")
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "edit-clear-symbolic")
        self.set_titlebar(self.header)
        self.header.pack_start(entry)
        self.add(self.header)

        entry.connect("icon-press", self.on_icon_click)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename="./download.jpeg", 
        width=1000, 
        height=1000, 
        preserve_aspect_ratio=True)

        self.image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.image.set_size_request(100, 100)
        print(self.image.set_from_pixbuf)
        self.add(self.image)




    def on_icon_click(self, widget, icon_pos, event):
        if(icon_pos == Gtk.EntryIconPosition.SECONDARY):
            widget.set_text("")
        else:
            text = widget.get_text()
            from urllib.request import urlopen,Request  
            from bs4 import BeautifulSoup
            import requests
            import re
            import os
            import time
            from PIL import Image
            from io import BytesIO
            from urllib.request import urlopen

            url = "https://wallhaven.cc/search?q=" + text + "&categories=110&purity=100&sorting=random&order=desc"
            print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            image_url = soup.find('img', {'class': 'lazyload'})["data-src"]
            print(image_url)
            image_name = "fetched_image" + ".jpg"
            image_path = os.path.join(os.getcwd(), image_name)
            print(image_path)
            with open(image_path, 'wb') as handle:
                response = requests.get(image_url, stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            image = Image.open(image_path)

            image = image.resize((800, 800), Image.ADAPTIVE)
            image.save(image_path)
            
            self.image.set_from_file(image_path)




    def on_button_clicked(self, widget):
        print("Hello World") 

window = Window()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()