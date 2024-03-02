def read_buildings(filename):
    buildings = []

    with open(filename) as f:
        result = f.read()

    result = result.strip("```\n").split("```\n")

    buildings_strings = []
    for blding in result:
        b = blding.rstrip("\n")
        buildings_strings.append(b)

    buildings_rows = []
    for bs in buildings_strings:
        buildings_rows.append(bs.split("\n"))

    for br in buildings_rows:
        building = []
        for row in br:
            building.append(row.split("|"))
        buildings.append(list(reversed(building)))

    return buildings

# Scoring section
def calculate_stone_score(building):
    score = 0
    for row_index, row in enumerate(building):
        for die in row:
            if str(die).startswith('S'):
                level = row_index + 1  # Level of the building
                if level == 1:
                    score += 2
                elif level == 2:
                    score += 3
                elif level == 3:
                    score += 5
                else:
                    score += 8
    return score


def calculate_adjecent_count(row, col, building):
    row_len = len(building[0])
    adjecents = []
    if row == 0:
        if col == 0:
            adjecents.append(building[row+1][col])
            adjecents.append(building[row][col+1])
        elif col == row_len - 1:
            adjecents.append(building[row][col-1])
            adjecents.append(building[row+1][col])
        else:
            adjecents.append(building[row][col-1])
            adjecents.append(building[row][col+1])
            adjecents.append(building[row+1][col])

    elif row == len(building)-1:
        if col == 0:
            adjecents.append(building[row][col+1])
            adjecents.append(building[row-1][col])
        elif col == row_len - 1:
            adjecents.append(building[row][col-1])
            adjecents.append(building[row-1][col])
        else:
            adjecents.append(building[row][col+1])
            adjecents.append(building[row][col-1])
            adjecents.append(building[row-1][col])

    else:
        if col == 0:
            adjecents.append(building[row][col+1])
            adjecents.append(building[row+1][col])
            adjecents.append(building[row-1][col])
        elif col == row_len - 1:
            adjecents.append(building[row][col-1])
            adjecents.append(building[row+1][col])
            adjecents.append(building[row-1][col])
        else:
            adjecents.append(building[row][col-1])
            adjecents.append(building[row][col+1])
            adjecents.append(building[row+1][col])
            adjecents.append(building[row-1][col])

    count = 0
    for ad in adjecents:
        if ad != "--":
            count += 1

    return count


def calculate_wood_score(building):
    score = 0
    for row_ind, level in enumerate(building):
        for col_ind, die in enumerate(level):
            if die.lower().startswith("w"):
                count = calculate_adjecent_count(row_ind, col_ind, building)
                score += count*2

    return score


def calculate_glass_score(building):
    score = 0
    for row in building:
        for die in row:
            if str(die).startswith("G"):
                score += int(die[1:])
    return score


def calculate_recycled_score(building):
    recycled_count = 0
    for row in building:
        for die in row:
            if str(die).startswith("R"):
                recycled_count += 1
    return [0, 2, 5, 10, 15, 20, 30][min(recycled_count, 6)]


def make_table(stone, wood, glass, recycled):
    total = stone + wood + glass + recycled
    rslt = f"+------------+------------+\n"\
        f"| stone      | {stone:<10} |\n"\
        f"| wood       | {wood:<10} |\n"\
        f"| glass      | {glass:<10} |\n"\
        f"| recycled   | {recycled:<10} |\n"\
        "+============|============+\n"\
        f"| Total      | {total:<10} |\n"\
        "+------------+------------+\n\n"

    return rslt


def input_buildings(buildings):
    return "\n".join([" ".join(row) for row in buildings])


def main():
    buildings = read_buildings("datafiles/buildings.txt")
    result = ""
    for building in buildings:
        wood = calculate_wood_score(building)
        glass = calculate_glass_score(building)
        recycled = calculate_recycled_score(building)
        stone = calculate_stone_score(building)
        result += input_buildings(building) + "\n"
        result += make_table(stone, wood, glass, recycled) + "\n"
    with open("datafiles/scoring-result.txt", "w") as output_file:
        output_file.write(result)


# Step 8: Execute the Main Function
if __name__ == "__main__":
   main()
