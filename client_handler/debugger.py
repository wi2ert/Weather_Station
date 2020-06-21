"""
This is the debugger message keeper used in server-client protocol
"""


class Debug:
    def __init__(self):
        self.messages = ["DEBUG RESPONSES:"]  # make a list of debug messages
        print("Debugger initialized")

    def __read(self):
        temp = self.messages.copy()
        self.messages = ["DEBUG RESPONSES:"]  # empty list of debug messages
        return temp  # return the original filled list

    def add(self, msg):
        self.messages.append(msg)  # add a message to the list of debug messages

    def __str__(self):
        # read and reset all debug messages, then convert them into a string with \n's
        messages = self.__read()
        res = ""
        for msg in messages:
            res += msg + "\n"
        return res.strip()  # strip last \n
