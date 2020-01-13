import kivy
kivy.require('1.11.1')

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

from tinydb import TinyDB, Query, where
db_rezepte = TinyDB('Datenbanken/Rezepte.json' , sort_keys=True, indent=4, separators=(',', ': '))
db_settings = TinyDB('Datenbanken/Settings.json' , sort_keys=True, indent=4, separators=(',', ': '))



class rezept_adder(Popup):
    def __init__(self, **kwargs):
        self.add_widget(Spirituosen_adder)



class Spirituosen_adder(BoxLayout):
    def __init__(self, **kwargs):
        pass
        