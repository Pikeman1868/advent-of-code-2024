
import re
import logging

def part1(input:str) -> int:
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input)
    result = 0
    for match in matches:
        logging.debug(match)
        result += int(match[0]) * int(match[1])
    return result


def part2(input:str) -> int:
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", input)
    result = 0
    enabled = True
    for match in matches:
        logging.debug(match)
        if match[3] == "don't()":
            enabled = False
        elif match[2] == "do()":
            enabled = True
        else:
            if enabled:
                result += int(match[0]) * int(match[1])
    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open("input.txt") as file:
        data = ""
        read = file.readlines()
        for line in read:
            data += line
        logging.debug(f"input: {data}")
        result = part1(data)
        logging.info(f"Part 1: {result}")
        result = part2(data)
        logging.info(f"Part 2: {result}")
