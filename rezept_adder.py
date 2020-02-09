from operator import itemgetter
from tinydb import TinyDB, Query, where
from kivy.factory import Factory
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
import kivy.properties as kivy_property
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.graphics import Color, Point
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.settings import Settings, SettingItem, SettingsPanel, SettingTitle
from kivy.config import ConfigParser
from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
import json
import kivy
kivy.require('1.11.1')

db_rezepte = TinyDB('Datenbanken/Rezepte.json',
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': '))
db_settings = TinyDB('Datenbanken/Settings.json',
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))



class rezept_adder(Popup):

    def weitere_Zutat(self):
        self.ids['rezept_adder_space'].add_widget(Zutaten_Selector())

    def on_pathchooser(self):
        pass



class Zutaten_Selector(GridLayout):
    Zutatenart = kivy_property.StringProperty()
    Zutatennummer = kivy_property.StringProperty()
    Zutat = kivy_property.StringProperty()
    zutaten_list = kivy_property.ListProperty(["-"])
    zutatenart_list = kivy_property.ListProperty(["-"])

    def __init__(self, **kwargs):
        super(Zutaten_Selector, self).__init__(**kwargs)

        with open('Zutaten_Dictionary.json') as JSON:
            json_dict = json.load(JSON)

        if not 'zutaten_nr' in globals():
            global zutaten_nr
            zutaten_nr = 1

        self.Zutatennummer = str(zutaten_nr)

        typen_liste = []

        for key in json_dict.keys():
            key_str = str(key)
            print(key_str)
            typen_liste.append(key_str.replace('_', ' ').capitalize())

        typen_liste.append("Bitte Typ wählen")

        self.zutatenart_list = typen_liste

    def on_zutatenart_spinner_select(self, text, name):
        with open('Zutaten_Dictionary.json') as JSON:
            json_dict = json.load(JSON)

        zutaten_liste = []

        text = ''.join([x[0].lower() + x[1:] for x in text])
        text = text.replace(' ', '_')
        print(text)

        for (key, value) in json_dict.items():
            if key == text:
                for (subkey, subvalue) in value.items():
                    print(subvalue)
                    zutaten_liste.append(subvalue)

        zutaten_liste.append("Bitte wählen")

        self.zutaten_list = zutaten_liste
