# Version 0.9.0
import kivy
kivy.require('1.11.1')

# Eigene Klassen
from rezept_adder import rezept_adder
from settings_panel import Fachinhalt_Setting, Calibration_Setting

# Sonstige Klassen
import json
import re

from JSON_Manager import JSON_Manager
from tinydb import TinyDB, Query, where
db_rezepte = TinyDB('Datenbanken/Rezepte.json' , sort_keys=True, indent=4, separators=(',', ': '))
db_settings = TinyDB('Datenbanken/Settings.json' , sort_keys=True, indent=4, separators=(',', ': '))

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.config import ConfigParser
from kivy.uix.settings import Settings, SettingItem, SettingsPanel, SettingTitle
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
import kivy.properties as kivy_property
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.dropdown import DropDown

Config.set('graphics', 'fullscreen', 'False')
Config.set('kivy', 'window_icon', 'GUI_Elemente/app_icon.png')

# Declaratons
sm = ScreenManager()

################################# Widgets
class Rezept(Popup):
    title = kivy_property.StringProperty()
    rezept = kivy_property.StringProperty()


class RecycleViewRow_Cocktails(BoxLayout):
    text = kivy_property.StringProperty()  
    image_source = kivy_property.StringProperty()
    rating = kivy_property.StringProperty()

    def show_rezept(self, cocktail_name):  
        text_rezept = ""

        rezept_geladen = DB_Helper().GET_Rezept_JSON(cocktail_name, 'cocktails')
        text_rezept = JSON_Manager().JSON_to_Rezept_String(rezept_geladen)

        popup_rezept = Rezept()
        popup_rezept.title = cocktail_name
        popup_rezept.rezept = text_rezept
        popup_rezept.open()



class RV_Cocktails(RecycleView):
    def __init__(self, **kwargs):
        super(RV_Cocktails, self).__init__(**kwargs)

        table = db_rezepte.table( 'cocktails' )   
    
        self.data = [{
            'text': json_object.get("name"),
            'image_source': json_object.get("image_path"),
            'rating': "Bewertung: " + str(json_object.get("rating")) + "/5",
            'id': str(json_object.get("id"))
            } for json_object in table]


#Alkoholfrei
class RecycleViewRow_Alkoholfrei(BoxLayout):
    text = kivy_property.StringProperty()  
    image_source = kivy_property.StringProperty()
    rating = kivy_property.StringProperty()

    def show_rezept(self, alkoholfrei_name):  
        text_rezept = ""
        
        rezept_geladen = DB_Helper().GET_Rezept_JSON(alkoholfrei_name, 'alkoholfrei')
        text_rezept = JSON_Manager().JSON_to_Rezept_String(rezept_geladen)

        popup_rezept = Rezept()
        popup_rezept.title = alkoholfrei_name
        popup_rezept.rezept = text_rezept
        popup_rezept.open()
        

class RV_Alkoholfrei(RecycleView):
    def __init__(self, **kwargs):
        super(RV_Alkoholfrei, self).__init__(**kwargs)
        
        table = db_rezepte.table( 'alkoholfrei' )   
    
        self.data = [{
            'text': json_object.get("name"),
            'image_source': json_object.get("image_path"),
            'rating': "Bewertung: " + str(json_object.get("rating")) + "/5",
            'id': str(json_object.get("id"))
            } for json_object in table]



class RecycleViewRow_Drinks(BoxLayout):
    text = kivy_property.StringProperty()  
    image_source = kivy_property.StringProperty()
    rating = kivy_property.StringProperty()
    drink_type = kivy_property.StringProperty()


class RV_Drinks(RecycleView):
    def __init__(self, **kwargs):
        super(RV_Drinks, self).__init__(**kwargs)
        
        table = db_rezepte.table( 'spirituosen' )   
    
        self.data = [{
            'text': json_object.get("name"),
            'drink_type': JSON_Manager.switch_zutaten(self, "alkohol", json_object.get("typ")) + ", " + str(json_object.get("vol_prozent")).replace(".", ",") + "% vol.",
            'image_source': json_object.get("image_path"),
            'rating': "Bewertung: " + str(json_object.get("rating")) + "/5",
            'id': str(json_object.get("id"))
            } for json_object in table]


###########################################################################
#---------------------------- Screens --------------------------------------
class Screen1(Screen):
    pass
        
class Screen2(Screen):
    pass

class Screen3(Screen):
    pass

class Screen4(Screen):
    def fullscreenchanger(self, value):
        if Window.fullscreen == False:
            Window.fullscreen = 'auto'
        else:
            Window.fullscreen = False

    def rezept_adder_open(self):
        print("Rezept_Adder wird geöffnet")
        popup_rezept_adder = rezept_adder()
        popup_rezept_adder.open()

    def rezept_editer_open(self):
        pass

###############################################################
class HomeScreen(BoxLayout): 
    def switch(self, to):

        if self.ids.sm.current == "screen1":
            current_screen = 1
        elif self.ids.sm.current == "screen2":
            current_screen = 2
        elif self.ids.sm.current == "screen3":
            current_screen = 3
        elif self.ids.sm.current == "screen4":
            current_screen = 4

        if current_screen == to:
            pass
        elif current_screen < to:
            self.ids.sm.transition = SlideTransition(direction='left')
        elif current_screen > to:
            self.ids.sm.transition = SlideTransition(direction='right')

        if to == 1 and current_screen > 2:
            self.ids.sm.current = "screen2"
            self.ids.sm.current = "screen1"
        elif to == 1:
            self.ids.sm.current = "screen1"
        elif to == 2:
            self.ids.sm.current = "screen2"
        elif to == 3:
            self.ids.sm.current = "screen3"
        elif to == 4 and current_screen < 3:
            self.ids.sm.current = "screen3"
            self.ids.sm.current = "screen4"
        elif to == 4:
            self.ids.sm.current = "screen4"
            
class DB_Helper():
    def GET_Rezept_JSON(self, rezeptname, rezepttyp):
        table = db_rezepte.table(rezepttyp)
        result_rezept = str(table.get(where('name') == rezeptname))
        json_rezept = str(result_rezept).replace("\'", "\"")
        rezept_geladen = json.loads(json_rezept)
        
        return rezept_geladen
            

#################################
class ZapfanlageApp(App):
    icon = 'GUI_Elemente/app_icon.png'
    title = 'Zapfanlage'

    def build(self):
        Builder.load_file('main.kv', encoding='utf8')
        return HomeScreen()

if __name__ == "__main__":
    ZapfanlageApp().run()