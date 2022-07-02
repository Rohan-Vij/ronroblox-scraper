"""Scraper(s) for the Rise of Nations Roblox wiki. Uses reST documentation format."""
import json

import requests
from bs4 import BeautifulSoup


class FormableScraper:
    """
    Rise of Nation Roblox formables wiki scraper.

    :param url: wiki URL to scrape from
    """

    def __init__(self, url):
        self.url = url
        self.formables_information = {}

        self.link_information = []

    def get_formables_list(self):
        """
        Get a list of formables and their wiki urls.
        """

        page = requests.get(self.url + "/wiki/Category:Formables")
        soup = BeautifulSoup(page.content, "html.parser")

        list_elements = soup.find_all(
            "li", class_="category-page__member")

        for element in list_elements:
            link = element.find("a", href=True)
            href = link['href']
            title = link['title']

            if "formable" not in title.lower():
                self.formables_information[title] = {"URL": self.url + href}
                self.link_information.append((href, title))

        return self.link_information

    def get_nation_information(self, tag):
        """
        Get a list of the required/start/etc nations for a formable.

        :param tag: the anchor tag class to search for
        """

        if not self.link_information:
            self.get_formables_list()

        for link in self.link_information:
            formable_page = requests.get(self.url + link[0])
            formable_soup = BeautifulSoup(formable_page.content, "html.parser")

            print(self.url + link[0])

            start_nations = formable_soup.find(
                "div", {"data-source": tag})

            # Can't exclude classes in BS4, so we have to find a list
            # of all the links and then exclude those with a class of "image"
            images = start_nations.find_all('a', {"class": "image"})
            all_links = start_nations.find_all('a')

            text_links = list(set(all_links).difference(images))

            self.formables_information[link[1]][tag.replace(" ", "_")] = [
                link.string for link in text_links]

        return self.formables_information

    def get_data(self):
        """
        Returns a dictionary of formable information.
        """

        return self.formables_information

    def write_to_file(self, filename):
        """
        Write the formable information to a JSON file.

        :param filename: The name of the JSON file (in the same directory) to write to.
        """

        with open(f"./{filename}", "w", encoding="utf-8") as file:
            json.dump(self.get_data(), file, sort_keys=True, indent=4)

        return "OK"


ronroblox = FormableScraper("https://ronroblox.fandom.com")

ronroblox.get_formables_list()

ronroblox.get_nation_information("start_nation")
ronroblox.get_nation_information("required")

ronroblox.write_to_file("formables.json")
