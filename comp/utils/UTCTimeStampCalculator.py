


class UTCTimeStampCalculator:
    
    SECONDS_IN_HOUR = 3600
    SECONDS_IN_DAY = SECONDS_IN_HOUR * 24    
    
    @staticmethod
    def days(value: int):
        if value < 0:
            raise ValueError("Invalid number of days")
        return UTCTimeStampCalculator.SECONDS_IN_DAY * value
    
    @staticmethod
    def hours(value: int):
        if value < 0:
            raise ValueError("Invalid number of hours")
        return UTCTimeStampCalculator.SECONDS_IN_HOUR * value