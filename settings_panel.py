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
db_rezepte = TinyDB('Datenbanken/Rezepte.json',
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': '))
db_settings = TinyDB('Datenbanken/Settings.json',
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))



class Fachinhalt_Setting(BoxLayout):
    text = kivy_property.StringProperty()
    fach_id = kivy_property.StringProperty()
    current_fachinhalt = kivy_property.StringProperty()
    drinks_list = kivy_property.ListProperty()

    def __init__(self, **kwargs):
        super(Fachinhalt_Setting, self).__init__(**kwargs)

        table_spirituosen = db_rezepte.table('spirituosen')

        if not 'fachlader_nr' in globals():
            global fachlader_nr
            fachlader_nr = 1

        self.fach_id = str(fachlader_nr)
        print('Aktuelle Fachinhalte werden geladen von Fach ' +
              str(fachlader_nr))

        gesetzt = False
        drinks_new_list = []

        for json_object in table_spirituosen:
            drinks_new_list.append(
                json_object.get("name") + ",  " +
                str(json_object.get("vol_prozent")).replace(".", ",") +
                "% vol.,  " + str(json_object.get("volumen")) + "ml")

        drinks_new_list.append("< Fach leer >")

        self.drinks_list = drinks_new_list

        result_fachinhalte = db_settings.get(where('name') == 'fachinhalte')
        id = result_fachinhalte.get("slot_" + str(fachlader_nr))
        print("Aktuelle ID des Drinks in Fach " + str(fachlader_nr) + ": ")
        print(id)

        if id != "null" and not gesetzt:
            doc = db_rezepte.table('spirituosen').get(doc_id=id)
            self.current_fachinhalt = doc.get("name") + ", " + str(
                doc.get("vol_prozent")) + "% vol., " + str(
                    doc.get("volumen")) + "ml"
            gesetzt = True
        elif not gesetzt:
            self.current_fachinhalt = "< Fach leer >"

        fachlader_nr = fachlader_nr + 1

    def on_spinner_select(self, text, fach_id):
        print(fach_id)
        print(text)

        result_fachinhalte = db_settings.get(where('name') == 'fachinhalte')

        id = result_fachinhalte.get("slot_" + fach_id)
        print("Aktuelle ID des Drinks in Fach " + fach_id + ": ")
        print(id)

        splitter_drink = result_drinks.split(",  |% vol.,  |ml", text)

        table_spirituosen = db_rezepte.table('spirituosen')
        result_drinks = table_spirituosen.get(
            (where('name') == splitter_drink[0])
            & (where('vol_prozent') == float(
                str(splitter_drink[1]).replace(',', '.')))
            & (where('volumen') == int(splitter_drink[2])))

        if result_drinks is not None:
            id = result_drinks.doc_id
            print(result_drinks)
            print(id)

        db_settings.update({"slot_" + fach_id: id},
                           where('name') == 'fachinhalte')



class Calibration_Setting(BoxLayout):
    text = kivy_property.StringProperty()
    fach_id = kivy_property.StringProperty()
    fach_id_plus = kivy_property.StringProperty()
    fach_id_minus = kivy_property.StringProperty()
    fach_id_plusplus = kivy_property.StringProperty()
    fach_id_minusminus = kivy_property.StringProperty()
    kalibrierungswert = kivy_property.StringProperty()
    color = kivy_property.ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(Calibration_Setting, self).__init__(**kwargs)

        if not 'fachkalibrierung_nr' in globals():
            global fachkalibrierung_nr
            fachkalibrierung_nr = 1

        self.fach_id = "Kalibrierung_Fach_" + str(fachkalibrierung_nr)
        self.fach_id_plus = "Kalibrierung_plus_Fach_" + str(
            fachkalibrierung_nr)
        self.fach_id_minus = "Kalibrierung_minus_Fach_" + str(
            fachkalibrierung_nr)
        self.fach_id_plusplus = "Kalibrierung_plusplus_Fach_" + str(
            fachkalibrierung_nr)
        self.fach_id_minusminus = "Kalibrierung_minusminus_Fach_" + str(
            fachkalibrierung_nr)

        print('Aktuelle Kalibrierungen werden geladen von Fach ' +
              str(fachkalibrierung_nr))

        result_kalibrierung = db_settings.get(where('name') == 'kalibrierung')
        kalibrierungswert = result_kalibrierung.get("slot_" +
                                                    str(fachkalibrierung_nr))

        print("Aktueller Kalibrierungswert der Spirituose in Fach " +
              str(fachkalibrierung_nr) + ": ")
        print(kalibrierungswert)

        self.kalibrierungswert = str(kalibrierungswert)

        fachkalibrierung_nr = fachkalibrierung_nr + 1

    def on_kalibration_select(self, id):
        id_bereinigt = str(id).replace('Kalibrierung_',
                                       '').replace('_Fach_', '')
        fach_nr = id_bereinigt.replace('plus', '').replace(
            'minus', '').replace('minusminus', '').replace('plusplus', '')
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

        self.color = [1, 0, 0, 1]
        self.kalibrierungswert = str(wert)

    def on_save_select(self, id):
        fach_id = str(id).replace('Kalibrierung_Fach_', '')
        kalibrierungswert = self.kalibrierungswert
        print(fach_id)
        print(kalibrierungswert)

        print('Aktuelle Kalibrierungen werden aktualisiert von Fach ' +
              str(fach_id))

        db_settings.update({"slot_" + fach_id: int(kalibrierungswert)},
                           where('name') == 'kalibrierung')

        result_kalibrierung = db_settings.get(where('name') == 'kalibrierung')
        kalibrierungswert = result_kalibrierung.get("slot_" + str(fach_id))

        print("Neuer Kalibrierungswert der Spirituose in Fach " + fach_id +
              ": ")
        print(kalibrierungswert)

        self.color = [1, 1, 1, 1]
        self.kalibrierungswert = str(kalibrierungswert)
