from typing import List, Protocol
import logging
import copy

class UnSafeReactorException(Exception):
    pass

class NoChangeException(UnSafeReactorException):
    pass

class NotIncreasingException(UnSafeReactorException):
    pass

class NotDecreasingException(UnSafeReactorException):
    pass

class MagnitudeException(UnSafeReactorException):
    pass

class Validator(Protocol):
    def verify_safe(self, reading:List[int]) -> bool:
        pass

class AbstractValidator(Validator):

    def verify_safe(self, reading:List[int]) -> bool:
        previous = 0
        current = 1
        is_safe = True
        try:
            while current < len(reading):
                self.verify_direction(reading[previous], reading[current])
                self.verify_magnitude(reading[previous], reading[current])
                previous = current
                current += 1
                
        except UnSafeReactorException as e:
            logging.info(msg="Reading unsafe", exc_info=e)
            is_safe = False

        return is_safe
   
    def verify_direction(self, previous:int, current:int):
        pass

    def verify_magnitude(self, previous:int, current:int):
        result = abs(previous - current)
        if result > 3:
            raise MagnitudeException(f"{result} > 3")


class ProxyValidator(Validator):
    def __init__(self, validator:AbstractValidator) -> None:
        super().__init__()
        self._validator: AbstractValidator = validator

    def verify_safe(self, reading:List[int]) -> bool:
        return self._validator.verify_safe(reading)
   
    def verify_direction(self, previous:int, current:int):
        self._validator.verify_direction(previous, current)

    def verify_magnitude(self, previous:int, current:int):
        self._validator.verify_magnitude(previous, current)
    

class Dampener(ProxyValidator):
    def __init__(self, validator: AbstractValidator) -> None:
        super().__init__(validator)
        self._dampened:bool = False

    def verify_safe(self, reading:List[int]) -> bool:
        self._dampened = False
        is_safe = super().verify_safe(reading)
        if not is_safe:
            for index_to_remove in range(len(reading)):
                modified_reading = copy.copy(reading)
                del modified_reading[index_to_remove]
                is_safe = super().verify_safe(modified_reading)
                if is_safe:
                    break

        return is_safe

class IncreasingValidator(AbstractValidator):
    def verify_direction(self, previous:int, current:int):
        if previous >= current:
            raise NotDecreasingException(f"{previous} >= {current}")  
        
class DecreasingValidator(AbstractValidator):
    def verify_direction(self, previous:int, current:int):
        if previous <= current:
            raise NotDecreasingException(f"{previous} <= {current}") 
    
class ValidatorFactory():
    def make(self, data:List[int]) -> AbstractValidator:
        pass

class DirectionValidatorFactory(ValidatorFactory):
    def make(self, data: List[int]) -> AbstractValidator:
        trend = 0
        for element in range(1, len(data)):
            result = data[element-1] - data[element]
            if result < 0:
                trend += 1
            elif result > 0:
                trend -=1
    
        if trend > 0:
            return IncreasingValidator()
        elif trend < 0:
            return DecreasingValidator()
        else:
            raise NoChangeException(f"{data[0]} == {data[1]}")
        
class DampenerValidatorFactory(DirectionValidatorFactory):
    def make(self, data: List[int]) -> AbstractValidator:
        return Dampener(super().make(data))

def is_day_safe(list:List[int], factory=DirectionValidatorFactory()) -> bool:
        try:
            direction_validator = factory.make(list)
            return direction_validator.verify_safe(list)
        except UnSafeReactorException:
            return False

def difference_elements(previous:int, current:int) -> int:
    return previous - current
        
def count_safe_reactor_days(data:str, dampener:bool=False) -> int:
    safe_days = 0
    data_by_day = parse_reactor_data(data)
    if dampener:
        factory = DampenerValidatorFactory()
    else :
        factory = DirectionValidatorFactory()
    for day in data_by_day:
        if is_day_safe(day, factory):
            safe_days += 1
    return safe_days


def parse_reactor_data(data:str) -> List[List[int]]:
    split_data = data.splitlines()
    data_by_day = []
    for reading in split_data:
        data_by_day.append([int(x) for x in reading.split()])
    return data_by_day



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with open("input.txt", "r") as f:
        data = f.read()
        print(count_safe_reactor_days(data))