from number_generator import RandomNumberGenerator

if __name__ == "__main__":
    number_generator = RandomNumberGenerator(1234567890)
    executors_count = number_generator.next_int(9, 20)
    tasks_count = executors_count
    cost = [[number_generator.next_int(1, 50) for _ in range(tasks_count)] for _ in range(executors_count)]
    with open("przydzial.dat", "w") as file:
        file.write(f"executors_count = {executors_count};\n")
        file.write(f"tasks_count = {tasks_count};\n")
        file.write("cost = [\n")
        for executor in range(executors_count):
            row = "\t["
            for task in range(tasks_count):
                row += f"{cost[executor][task]},"
            row = row.rstrip(",")
            row += "],\n"
            file.write(row)
        file.write("];")
