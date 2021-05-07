from PIL import ImageGrab, ImageOps
import pytesseract
import re

# Apparently pytesseract is too dumb to find the path itself so we gotta tell it where to go
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# A basic class to store champion name, and two dicts with summoner spell names and their last used game time
class Summoner:
    champion_name = ""
    summoner_one = {"spell": "", "last_used": ""}
    summoner_two = {"spell": "", "last_used": ""}

    def __init__(self, champion_name):
        """
        Constructor for Summoner
        :param champion_name: Name of champion
        :type champion_name: String
        """
        self.champion_name = champion_name
        self.summoner_one = {"spell": "", "last_used": ""}
        self.summoner_two = {"spell": "", "last_used": ""}


# A class for the chat window in the game
class ChatWindow:
    # Coordinates of the chat window in game
    top_left_coord = 0, 0
    bottom_right_coord = 0, 0

    # Messages in the chat window
    messages = []

    # Dict of champion names: Summoner object
    champions = {}

    def __init__(self, top_left_coord, bottom_right_coord):
        """
        Constructor for ChatWindow
        :param top_left_coord: Coordinates of top left of chat window in the game
        :type top_left_coord: Int Tuple
        :param bottom_right_coord: Coordinates of bottom right of chat window in the game
        :type bottom_right_coord: Int Tuple
        """
        self.top_left_coord = top_left_coord
        self.bottom_right_coord = bottom_right_coord
        self.messages = []
        self.champions = {}
        self.read_chat()

    def read_chat(self):
        """
        OCRs the chat into the message list
        :return: null
        :rtype: null
        """
        self.messages = []
        chat_image = self.get_image()
        text_chat = pytesseract.image_to_string(chat_image)
        for message in text_chat.split('\n'):
            if message != '':
                self.messages.append(message)
        self.summoner_check()

    def get_image(self):
        """
        Grabs an image of the ChatWindow and grayscales it
        :return: Image at top_left_coord, bottom_right_coord
        :rtype: ImageGrab.Grab
        """
        # Place holder test image
        img = ImageGrab.grab(bbox=(
            self.top_left_coord[0], self.top_left_coord[1], self.bottom_right_coord[0], self.bottom_right_coord[1]))
        ImageOps.grayscale(img)
        return img

    def summoner_check(self):
        """
        Populates the champion dictionary with the most recent ping for their spells
        :return: null
        :rtype: null
        """
        # Regex to check and see if the message is pinging a summoner spell
        summoner_ping_re = re.compile(r"(?P<timestamp>\[[0-9]{2}:[0-9]{2}]) (?P<player_name>[a-zA-Z]+) ("
                                      r"?P<player_champion>\([a-zA-z]+\)): (?P<champion>[a-zA-Z]+) ("
                                      r"?P<spell>Barrier|Clarity|Cleanse|Exhaust|Flash|Ghost|Heal|Ignite|Teleport"
                                      r"|Smite)")
        for message in self.messages:
            # print(message)
            summoner_ping = summoner_ping_re.match(message)
            if summoner_ping:
                # If champions dict is empty add it as first entry, I think there has got to be a better way to do this
                # check, but I'm dumb
                if len(self.champions) == 0:
                    self.champions[summoner_ping.group("champion")] = Summoner(summoner_ping.group("champion"))
                    self.champions[summoner_ping.group("champion")].summoner_one["spell"] = summoner_ping.group("spell")
                    self.champions[summoner_ping.group("champion")].summoner_one["last_used"] = \
                        summoner_ping.group("timestamp")
                else:
                    # If they are already in the dict
                    if summoner_ping.group("champion") in self.champions:
                        # Check and update last used on first summoner if the summoner is the same
                        if self.champions[summoner_ping.group("champion")].summoner_one["spell"] == \
                                summoner_ping.group("spell"):
                            self.champions[summoner_ping.group("champion")].summoner_one["last_used"] = \
                                summoner_ping.group("timestamp")
                        # Check and update last used on second summoner if the summoner is the same
                        elif self.champions[summoner_ping.group("champion")].summoner_two["spell"] == \
                                summoner_ping.group("spell"):
                            self.champions[summoner_ping.group("champion")].summoner_two["last_used"] = \
                                summoner_ping.group("timestamp")
                        # If they are already in the dict, but didn't trip the second spell check, you can assume that
                        # the first spell is populated already, but the second isn't so just populate the second
                        else:
                            self.champions[summoner_ping.group("champion")].summoner_two["spell"] = \
                                summoner_ping.group("spell")
                            self.champions[summoner_ping.group("champion")].summoner_two["last_used"] = \
                                summoner_ping.group("timestamp")
                    else:
                        # print(summoner_ping.group("champion"), "not in dict already")
                        self.champions[summoner_ping.group("champion")] = Summoner(summoner_ping.group("champion"))
                        self.champions[summoner_ping.group("champion")].summoner_one["spell"] = \
                            summoner_ping.group("spell")
                        self.champions[summoner_ping.group("champion")].summoner_one["last_used"] = \
                            summoner_ping.group("timestamp")
