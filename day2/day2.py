from typing import List

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

class Validator:
    def verify_direction(self, previous:int, current:List[int]):
        pass

    def verify_magnitude(self, previous:int, current:List[int]):
        if len(current) > 0 and abs(previous - current[0]) > 3:
            raise MagnitudeException(f"{abs(previous - current[0])} > 3")

class ProxyValidator(Validator):
    def __init__(self, validator:Validator) -> None:
        super().__init__()
        self._validator: Validator = validator

class Dampener(ProxyValidator):
    def __init__(self, validator: Validator) -> None:
        super().__init__(validator)

    def verify_magnitude(self, previous: int, current: List[int]): 
        try:
            self._validator.verify_magnitude(previous, current)
        except UnSafeReactorException:
            self._validator.verify_magnitude(previous, current[1:])
    
    def verify_direction(self, previous: int, current: List[int]):
        try:
            self._validator.verify_direction(previous, current)
        except UnSafeReactorException:
            self._validator.verify_direction(previous, current[1:])

class IncreasingValidator(Validator):
    def verify_direction(self, previous:int, current:List[int]):
        if len(current) > 0 and previous >= current[0]:
            raise NotIncreasingException(f"{previous} > {current[0]}")  
        
class DecreasingValidator(Validator):
    def verify_direction(self, previous:int, current:List[int]):
        if len(current) > 0 and previous <= current[0]:
            raise NotDecreasingException(f"{previous} < {current[0]}") 
    
class ValidatorFactory():
    def make(self, data:List[int]) -> Validator:
        pass

class DirectionValidatorFactory(ValidatorFactory):
    def make(self, data: List[int]) -> Validator:
        if data[0] < data[1]:
            return IncreasingValidator()
        elif data[0] > data[1]:
            return DecreasingValidator()
        else:
            raise NoChangeException(f"{data[0]} == {data[1]}")
        
class DampenerValidatorFactory(DirectionValidatorFactory):
    def make(self, data: List[int]) -> Validator:
        return Dampener(super().make(data))

def is_day_safe(list:List[int], factory=DirectionValidatorFactory()) -> bool:
    try:
        # Deterimer direction
        direction_validator = factory.make(list)
        verify_safe(list[0], list[1:], direction_validator)

        return True
    except UnSafeReactorException:
        return False

def difference_elements(previous:int, current:int) -> int:
    return previous - current


def verify_safe(previous:int, remaining:List[int], validation:Validator):
    validation.verify_direction(previous, remaining)
    validation.verify_magnitude(previous, remaining)
    if len(remaining) > 1:
        verify_safe(remaining[0], remaining[1:], validation)
        
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
    with open("input.txt", "r") as f:
        data = f.read()
        print(count_safe_reactor_days(data))