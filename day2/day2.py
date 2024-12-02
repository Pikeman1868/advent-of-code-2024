from typing import List

class UnSafeReactorException(Exception):
    pass

class NoChangeException(UnSafeReactorException):
    pass

class NotIncreasingException(UnSafeReactorException):
    pass

class NotDecreasingException(UnSafeReactorException):
    pass

class Validator:
    def verify_direction(self, previous:int, current:int):
        pass

    def verify_magnitude(self, previous:int, current:int):
        if abs(previous - current) > 3:
            raise NotDecreasingException(f"{abs(previous - current)} > 3")
    
class IncreasingValidator(Validator):
    def verify_direction(self, previous:int, current:int):
        if not previous < current:
            raise NotIncreasingException(f"{previous} > {current}")  
        
class DecreasingValidator(Validator):
    def verify_direction(self, previous:int, current:int):
        if not previous > current:
            raise NotDecreasingException(f"{previous} < {current}") 

def is_day_safe(list:List[int]) -> bool:
    try:
        # Deterimer direction
        direction_validator = determine_direction(list)
        verify_safe(list[0], list[1:], direction_validator)

        return True
    except UnSafeReactorException:
        return False


def determine_direction(list:List[int]) -> Validator:
    if list[0] < list[1]:
        return IncreasingValidator()
    elif list[0] > list[1]:
        return DecreasingValidator()
    else:
        raise NoChangeException(f"{list[0]} == {list[1]}")

def difference_elements(previous:int, current:int) -> int:
    return previous - current


def verify_safe(previous:int, remaining:List[int], validation:Validator):
    validation.verify_direction(previous, remaining[0])
    validation.verify_magnitude(previous, remaining[0])
    if len(remaining) > 1:
        verify_safe(remaining[0], remaining[1:], validation)
        
def count_safe_reactor_days(data:str) -> int:
    safe_days = 0
    data_by_day = parse_reactor_data(data)
    for day in data_by_day:
        if is_day_safe(day):
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