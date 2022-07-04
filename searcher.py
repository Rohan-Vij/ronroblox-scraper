"""JSON searcher for formables from the Rise of Nations wiki. Uses reST documentation format."""

import json


class FormablesSearcher:
    """
    Rise of Nation Roblox formables JSON searcher.

    :param filename: JSON filename to search in
    """

    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def load_json(self):
        """
        Load the content of the JSON file into a dictionary.
        """
        with open(f"./{self.filename}", "r", encoding="utf-8") as file:
            self.data = json.load(file)

        return "OK"

    def sort_by_greatest_or_lowest_attribute(self, attribute, direction):
        """
        Sort by the greatest or lowest number of start nations.

        :param attribute: the dictionary attribute (a list) to sort by
        :param direction: the direction to sort by (lowest = lowest --> greatest, vice versa)
        """
        res = sorted(self.data, key=lambda key: len(self.data[key][attribute]))

        if direction == "lowest":
            return res
        if direction == "greatest":
            return list(reversed(res))
        return res

    def write_to_file(self, filename, lst):
        """
        Write the formable information to a JSON file.

        :param filename: The name of the JSON file (in the same directory) to write to
        :param lst: A list of keys to add to the JSON file
        """

        data = {}
        for key in lst:
            data[key] = self.data[key]
            data[key]["completed"] = False

        with open(f"./{filename}", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return "OK"


searcher = FormablesSearcher("formables.json")

searcher.load_json()

searcher.write_to_file(
    "searched.json", searcher.sort_by_greatest_or_lowest_attribute("required", "lowest"))
