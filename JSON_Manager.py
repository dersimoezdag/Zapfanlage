import json

class JSON_Manager():
    def __init__(self):
        pass

    def SQL_to_JSON(self, sql_data):
        sql_data = sql_data.replace("\\r\\n", " ")
        sql_data = sql_data.replace("('", "")
        sql_data = sql_data.replace("',)", "")
        sql_data = sql_data.replace("'", '"')
        sql_data = sql_data.replace('\t','')
        sql_data = sql_data.replace('\n','')
        sql_data = sql_data.replace(',}','}')
        sql_data = sql_data.replace(',]',']')
        return sql_data

    def JSON_to_Rezept_String(self, json_rezept):
        rezept_string = ""
        for (key, value) in json_rezept.items():

            if key == "beschreibung":
                rezept_string = rezept_string + "\n" + value + "\n\n"
            
            if key == "ingredients":
                for (key, value) in value.items():
                    
                    if key == "spirituosen":
                        for (key, value) in value.items():
                            temp = self.switch_zutaten("alkohol", key)
                            if temp != "invalid":
                                rezept_string = rezept_string + temp + ":  " + str(value) + " cl \n"

                    if key == "filler":
                        for (key, value) in value.items():
                            temp = self.switch_zutaten("softdrinks", key)
                            if temp != "invalid":
                                rezept_string = rezept_string + temp + ":  " + str(value) + " cl \n"
                                
                    temp = self.switch_zutaten("feste_zutaten", key)
                    if temp != "invalid":
                        rezept_string = rezept_string + temp + ":  " + str(value) + " \n"

                    if key == "garnitur":
                        rezept_string = rezept_string + "Garnitur:  "
                        for i in value:
                            temp = self.switch_zutaten("garnitur",i)
                            rezept_string = rezept_string + str(temp) + ", "
                        rezept_string = rezept_string[:-2]

            if key == "zubereitung":
                rezept_string = rezept_string + "\n\n" + value

        return rezept_string



    ######### Swtches für Cocktailrezepte
    def switch_zutaten(self, type, argument):
        json_dict = ""

        with open('Zutaten_Dictionary.json') as JSON:
            json_dict = json.load(JSON)
            
            if type in json_dict:
                if argument in json_dict[type]:
                    return json_dict[type][argument]
                else:
                    return "invalid"
            else:
                return "invalid"