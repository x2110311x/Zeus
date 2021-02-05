import datetime

class Utilities():
    def msdiff(t1, t2):
        difftime = t2 - t1  # find the difference
        datetime.timedelta(0, 4, 316543)
        diffms = int(difftime.microseconds / 1000)  # convert to milliseconds
        return diffms