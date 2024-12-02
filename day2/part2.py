from day2 import count_safe_reactor_days


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()
        print(count_safe_reactor_days(data, dampener=True))