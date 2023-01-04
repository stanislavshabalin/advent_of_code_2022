import os


class Register:
    def __init__(self, cycle_listener):
        self._cycle = 0
        self._value = 1
        self.cycle_listener = cycle_listener

    def _notify_listener(self, cycle, value):
        self.cycle_listener.notify(cycle=cycle, register_value=value)

    def do_command(self, command, *args):
        if command == "noop":
            self._cycle += 1
            self._notify_listener(self._cycle, self._value)
        elif command == "addx":
            for _ in range(2):
                self._cycle += 1
                self._notify_listener(self._cycle, self._value)

            self._value += args[0]


class CycleListener:
    def __init__(self):
        pass

    def notify(self, cycle, register_value):
        crt_position = (cycle - 1) % 40
        if register_value - 1 <= crt_position <= register_value + 1:
            print("#", end="")
        else:
            print(".", end="")

        if cycle % 40 == 0:
            print("\n", end="")


def main(input_file):
    listener = CycleListener()
    register = Register(listener)

    for line in input_file:
        splitted_line = line.split()
        command = splitted_line[0]
        args = []
        if len(splitted_line) > 1:
            args = map(int, splitted_line[1:])

        register.do_command(command, *args)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "10.txt")
    with open(file_path, "r") as input_file:
        main(input_file)
