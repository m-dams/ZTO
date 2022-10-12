from number_generator import RandomNumberGenerator


if __name__ == "__main__":
    number_generator = RandomNumberGenerator(1234567890)

    items_count = number_generator.next_int(9, 20)
    backpack_volume = number_generator.next_int(items_count, items_count*4)
    items_features = [[number_generator.next_int(1, 10), number_generator.next_int(1, 10), number_generator.next_int(1, 10)] for _ in range(items_count)]
    with open("dwuplecak.dat", "w") as f:
        f.write(f"items_count = {items_count};\n")
        f.write(f"backpack_volume = {backpack_volume};\n")
        f.write(f"items_features = [\n")
        for item in range(items_count):
            row = "\t["
            for feature in range(3):
                row += f"{items_features[item][feature]},"
            row = row.rstrip(",")
            row += "],\n"
            f.write(row)
        f.write("];")