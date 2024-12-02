import sys
from typing import List, Dict


def parse(input: List[str]) -> List[List[int]]:
    left_list = []
    right_list =[]
    for line in input:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))
    return (left_list, right_list)

def diff_lists(left_list: List[int], right_list: List[int]) -> List[int]:
    differences = []
    for i in range(len(left_list)):
        differences.append(abs(left_list[i] - right_list[i]))
    return differences


def part_1(left_list: List[str], right_list: List[str]) -> int:
    #sort   
    left_list.sort()
    right_list.sort()

    #find differences of indexes
    differences = diff_lists(left_list, right_list)
    #sum differences
    return sum(differences)

def map_unqiue(right_list: List[int]) -> Dict[int, int]:
    right_map = {}
    for i in range(len(right_list)):
        if right_list[i] in right_map:
            right_map[right_list[i]] += 1
        else:
            right_map[right_list[i]] = 1
    return right_map

def get_multiples(left_list: List[int], right_map: Dict[int, int]) -> int:
    result = []
    for i in left_list:
        multiple = 0
        try: 
            multiple = right_map[i]
        except:
            multiple = 0
        result.append(i*multiple)
    return result
        
def part2(left_list: List[str], right_list: List[str]) -> int:
    right_map = map_unqiue(right_list)
    result = get_multiples(left_list, right_map)
    return sum(result)

def main(input: List[str]) -> int:
    #paser inputs
    (left_list, right_list) = parse(input)
    return part2(left_list, right_list)
    
    


if __name__ == "__main__":
    
    #Read File
    with open("input.txt", "r") as f:
        input = f.read().splitlines()
        result = main(input)
        print(f"Result: {result}")