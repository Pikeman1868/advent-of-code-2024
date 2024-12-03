from typing import List, Protocol
import logging

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
    def verify_safe(self) -> bool:
        pass

class AbstractValidator(Validator):
    def __init__(self, data:List[int]):
        self._data:List[int] = data
        self._previous:int = 0
        self._current:int = 0

    @property
    def previous(self) -> int:
        return self._previous
    
    @previous.setter
    def previous(self, index:int) :
        self._previous = index

    @property
    def current(self) -> int:
        return self._current
    
    @current.setter
    def current(self, index:int) :
        self._current = index

    @property
    def data(self) -> List[int]:
        return self._data

    def verify_safe(self) -> bool:
        self.previous = 0
        self.current = 1
        is_safe = True
        try:
            while self.current < len(self.data):
                self.verify_direction()
                self.verify_magnitude()
                self.previous = self.current
                self.current += 1
                
        except UnSafeReactorException as e:
            logging.info(msg="Reading unsafe", exc_info=e)
            is_safe = False

        return is_safe
   
    def verify_direction(self):
        pass

    def verify_magnitude(self):
        previous_reading = self.data[self.previous]
        current_reading = self.data[self.current]
        result = abs(previous_reading - current_reading)
        if result > 3:
            raise MagnitudeException(f"{result} > 3")


class ProxyValidator(Validator):
    def __init__(self, validator:AbstractValidator) -> None:
        super().__init__()
        self._validator: AbstractValidator = validator

    @property
    def previous(self) -> int:
        return self._validator.previous
    
    @previous.setter
    def previous(self, index:int) :
        self._validator.previous = index

    @property
    def current(self) -> int:
        return self._validator._current
    
    @current.setter
    def current(self, index:int) :
        self._validator._current = index

    @property
    def data(self) -> List[int]:
        return self._validator._data

    def verify_safe(self) -> bool:
        self.previous = 0
        self.current = 1
        is_safe = True
        try:
            while self.current < len(self.data):
                self.verify_direction()
                self.verify_magnitude()
                self.previous = self.current
                self.current += 1
                
        except UnSafeReactorException as e:
            logging.info(msg="Reading unsafe", exc_info=e)
            is_safe = False

        return is_safe
   
    def verify_direction(self):
        self._validator.verify_direction()

    def verify_magnitude(self):
        self._validator.verify_magnitude()
    

class Dampener(ProxyValidator):
    def __init__(self, validator: AbstractValidator) -> None:
        super().__init__(validator)
        self._dampened:bool = False

    def verify_safe(self) -> bool:
        self._dampened = False
        return super().verify_safe()

    def verify_magnitude(self): 
        try:
            self._validator.verify_magnitude()
        except UnSafeReactorException as e:
            logging.info(msg="Value unsafe... applying dampenin", exc_info=e)
            self._dampen(self._validator.verify_magnitude, e)
    
    def verify_direction(self):
        try:
            self._validator.verify_direction()
        except UnSafeReactorException as e: 
            logging.info(msg="Value unsafe... applying dampenin", exc_info=e)  
            self._dampen(self._validator.verify_direction, e)

    def _dampen(self, func, e:UnSafeReactorException):
        if not self._dampened:
            self._dampened = True
            
            if self.current < len(self.data)-1:
                self.current += 1 #skip element
                func()
        else:
            raise e # Rethrow

class IncreasingValidator(AbstractValidator):
    def verify_direction(self):
        previous_reading = self.data[self.previous]
        current_reading = self.data[self.current]
        if previous_reading >= current_reading:
            raise NotDecreasingException(f"{previous_reading} >= {current_reading}")  
        
class DecreasingValidator(AbstractValidator):
    def verify_direction(self):
        previous_reading = self.data[self.previous]
        current_reading = self.data[self.current]
        if previous_reading <= current_reading:
            raise NotDecreasingException(f"{previous_reading} <= {current_reading}") 
    
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
            return IncreasingValidator(data)
        elif trend < 0:
            return DecreasingValidator(data)
        else:
            raise NoChangeException(f"{data[0]} == {data[1]}")
        
class DampenerValidatorFactory(DirectionValidatorFactory):
    def make(self, data: List[int]) -> AbstractValidator:
        return Dampener(super().make(data))

def is_day_safe(list:List[int], factory=DirectionValidatorFactory()) -> bool:
        try:
            direction_validator = factory.make(list)
            return direction_validator.verify_safe()
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