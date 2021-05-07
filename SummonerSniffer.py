from LeagueStuff import ChatWindow
import keyboard

# Int Tuples for chat window coordinates. Hard coded values, updated these yourself based on monitor size and chat
# position.
TOP_LEFT_COORD = 20, 720
BOTTOM_RIGHT_COORD = 700, 1355

# Hot key to press when you want the program to run.
REPORT_HOTKEY = '/ + .'

# Dictionary of summoner spell cool downs
SUMMONER_CDS = {
    "Barrier": 180,
    "Clarity": 240,
    "Cleanse": 210,
    "Exhaust": 210,
    "Flash": 300,
    "Ghost": 210,
    "Heal": 240,
    "Ignite": 180,
    "Teleport": 420,  # this scales with level, not sure how to handle this, for now just using max CD
    "Smite": 15
}


def main():
    """
    Main
    :return: 0
    :rtype: int
    """
    while True:
        keyboard.wait(REPORT_HOTKEY)
        chat = ChatWindow(TOP_LEFT_COORD, BOTTOM_RIGHT_COORD)
        # print('\n' * 10)
        try:
            # print("trying report")
            print_report(chat)
        except KeyError:
            print("Something went weird somewhere")


def print_report(chat):
    """
    Prints out a report to the console about when summoner spells will be up
    :param chat: A chat object
    :type chat: ChatWindow
    :return: null
    :rtype: null
    """
    print(chat.champions)
    for champion in chat.champions:
        try:
            print(champion)
            last_use = chat.champions[champion].summoner_one["last_used"]
            up_at = second_math(last_use, SUMMONER_CDS[chat.champions[champion].summoner_one["spell"]])
            print(chat.champions[champion].summoner_one["spell"], "up at:", up_at)
            last_use = chat.champions[champion].summoner_two["last_used"]
            up_at = second_math(last_use, SUMMONER_CDS[chat.champions[champion].summoner_two["spell"]])
            print(chat.champions[champion].summoner_two["spell"], "up at:", up_at)
        except KeyError:
            print("KeyError, potential OCR issue, potentially no second summoner")


def second_math(time, seconds_add):
    """
    Converts minutes and seconds in mm:ss format for seconds, adds seconds, converts back to mm:ss and returns
    :param time: The initial time you want added to
    :type time: String
    :param seconds_add: The number of seconds you want added
    :type seconds_add: String
    :return: time + seconds_add in mm:ss
    :rtype: String
    """
    minutes = int(time[1:3]) * 60
    seconds = int(time[4:6])
    time_seconds = minutes + seconds + int(seconds_add)
    minutes = int(time_seconds / 60)
    seconds = int(time_seconds % 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if minutes < 10:
        minutes = '0' + str(minutes)

    time_seconds = str(minutes) + ":" + str(seconds)
    return time_seconds


if __name__ == '__main__':
    main()
