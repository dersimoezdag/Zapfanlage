# Version 0.8.4

import kivy
kivy.require('1.11.1')

# Eigene Klassen
from Database_Manager import DatabaseManager
from JSON_Manager import JSON_Manager
from tinydb import TinyDB, Query, where
db_rezepte = TinyDB('Rezepte.json' , sort_keys=True, indent=4, separators=(',', ': '))
db_settings = TinyDB('Settings.json' , sort_keys=True, indent=4, separators=(',', ': '))

# Sonstige Klassen
import json
import re

from kivy.app import App
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

class cocktail_adder(Popup):
    pass


class RecycleViewRow_Cocktails(BoxLayout):
    text = kivy_property.StringProperty()  
    image_source = kivy_property.StringProperty()
    rating = kivy_property.StringProperty()

    def show_rezept(self, cocktail_name):  
        text_rezept = ""

        rezept_path = DatabaseManager().get_cocktail_rezept(cocktail_name)
        with open(rezept_path.replace("('", "").replace("',)", "")) as JSON:
            rezept_geladen = json.load(JSON)

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

        rezept_path = DatabaseManager().get_alkoholfrei_rezept(alkoholfrei_name)
        with open(rezept_path.replace("('", "").replace("',)", "")) as JSON:
            rezept_geladen = json.load(JSON)

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

    def cockatil_adder(self):
        popup_cocktail_adder = cocktail_adder()
        popup_cocktail_adder.open()

    def cockatil_editer(self):
        pass

#----------------------------
class Fachinhalt_Setting(BoxLayout):
    text = kivy_property.StringProperty()
    fach_id = kivy_property.StringProperty()
    current_fachinhalt = kivy_property.StringProperty()
    drinks_list = kivy_property.ListProperty()

    def __init__(self, **kwargs):
        super(Fachinhalt_Setting, self).__init__(**kwargs)

        table_spirituosen = db_rezepte.table( 'spirituosen' )
        
        if not 'fachlader_nr' in globals():
           global fachlader_nr 
           fachlader_nr = 1

        self.fach_id = str(fachlader_nr)
        print ('Aktuelle Fachinhalte werden geladen von Fach ' + str(fachlader_nr))
        
        gesetzt = False
        drinks_new_list = []

        for json_object in table_spirituosen:
            drinks_new_list.append(json_object.get("name") + ",  " +
                str(json_object.get("vol_prozent")).replace(".", ",") + "% vol.,  " + 
                str(json_object.get("volumen")) + "ml")
            
        drinks_new_list.append("< Fach leer >")

        self.drinks_list = drinks_new_list
        
        result_fachinhalte = db_settings.get(where('name') == 'fachinhalte')
        id = result_fachinhalte.get("slot_" + str(fachlader_nr))
        print("Aktuelle ID des Drinks in Fach " + str(fachlader_nr) + ": ")
        print(id)
        
        if id != "null" and not gesetzt:
            doc = db_rezepte.table( 'spirituosen' ).get(doc_id = id)
            self.current_fachinhalt = doc.get("name") + ", " + str(doc.get("vol_prozent")) + "% vol., " + str(doc.get("volumen")) + "ml"
            gesetzt = True
        elif not gesetzt:
            self.current_fachinhalt = "< Fach leer >"

        

        fachlader_nr = fachlader_nr + 1

    def on_spinner_select(self, text, fach_id):
        print (fach_id)
        print (text)
        
        result_fachinhalte = db_settings.get(where('name') == 'fachinhalte')
        
        id = result_fachinhalte.get("slot_" + fach_id)
        print("Aktuelle ID des Drinks in Fach " + fach_id + ": ")
        print(id)
        
        splitter_drink = re.split(",  |% vol.,  |ml", text)
 
        table_spirituosen = db_rezepte.table('spirituosen')
        result_drinks = table_spirituosen.get((where('name') == splitter_drink[0]) & (where('vol_prozent') == float(str(splitter_drink[1]).replace(',', '.'))) & (where('volumen') == int(splitter_drink[2])))
        
        if result_drinks is not None:
            id = result_drinks.doc_id
            print(result_drinks)
            print(id)

        db_settings.update({"slot_" + fach_id : id}, where('name') == 'fachinhalte')
            
            
class Calibration_Setting(BoxLayout):
    text = kivy_property.StringProperty()
    fach_id = kivy_property.StringProperty()
    fach_id_plus = kivy_property.StringProperty()
    fach_id_minus = kivy_property.StringProperty()
    fach_id_plusplus = kivy_property.StringProperty()
    fach_id_minusminus = kivy_property.StringProperty()
    kalibrierungswert = kivy_property.StringProperty()

    def __init__(self, **kwargs):
        super(Calibration_Setting, self).__init__(**kwargs)

        if not 'fachkalibrierung' in globals():
            global fachkalibrierung 
            fachkalibrierung = 1

        self.fach_id = "Kalibrierung_Fach_" + str(fachkalibrierung)
        self.fach_id_plus = "Kalibrierung_plus_Fach_" + str(fachkalibrierung)
        self.fach_id_minus = "Kalibrierung_minus_Fach_" + str(fachkalibrierung)
        self.fach_id_plusplus = "Kalibrierung_plusplus_Fach_" + str(fachkalibrierung)
        self.fach_id_minusminus = "Kalibrierung_minusminus_Fach_" + str(fachkalibrierung)

        kalibrierungswert = str(DatabaseManager().get_setting("kalibration_" + str(fachkalibrierung)))
        
        print(kalibrierungswert)

        self.kalibrierungswert = kalibrierungswert.replace('[(', '').replace(',)]', '').replace("'", '')

        print ('Aktuelle Kalibrierungen werden geladen von Fach ' + str(fachkalibrierung))

        fachkalibrierung = fachkalibrierung + 1


    def on_kalibration_select(self, id):    
        id_bereinigt = str(id).replace('Kalibrierung_','').replace('_Fach_','')
        fach_nr = id_bereinigt.replace('plus','').replace('minus','').replace('minusminus','').replace('plusplus','')
        plus_or_minus = id_bereinigt.replace(fach_nr, '')

        print(fach_nr)

        wert = int(self.kalibrierungswert)

        print(wert)

        if plus_or_minus == 'plus':
            wert = wert + 1
        elif plus_or_minus == 'minus':
            wert = wert - 1
        elif plus_or_minus == 'plusplus':
            wert = wert + 10
        elif plus_or_minus == 'minusminus':
            wert = wert - 10

        print(wert)
        
        self.kalibrierungswert = str(wert)


    def on_save_select(self, id):
        id_bereinigt = str(id).replace('Kalibrierung_Fach_','')
        wert = self.kalibrierungswert
        print(id_bereinigt)
        print(wert)
        DatabaseManager().set_setting("kalibration_" + str(id_bereinigt),str(wert))

        wert = str(DatabaseManager().get_setting("kalibration_" + str(id_bereinigt)))
        wert = wert.replace('[(', '').replace(',)]', '').replace("'", '')
        print(wert)
        
        self.kalibrierungswert = wert        



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
            

#################################
class ZapfanlageApp(App):
    icon = 'GUI_Elemente/app_icon.png'
    title = 'Zapfanlage'

    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    ZapfanlageApp().run()