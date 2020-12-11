import random

total_game_count = int(input("How many games? "))
print_output = input("Print output? (slower) ") == "y"

total_win_count = 0
magic_game_count = {
    4: 0,
    5: 0,
    6: 0,
    8: 0,
    9: 0,
    10: 0
}
magic_win_count = {
    4: 0,
    5: 0,
    6: 0,
    8: 0,
    9: 0,
    10: 0
}
roll_count_distribution = [0] * 999


# Roll two dice and get the sum
def roll():
    return random.randint(1, 6) + random.randint(1, 6)


for i in range(total_game_count):
    # Play the game!
    rolls = [roll()]
    if rolls[0] == 7 or rolls[0] == 11:
        win = True
    elif rolls[0] == 2 or rolls[0] == 3 or rolls[0] == 12:
        win = False
    else:
        magic_game_count[rolls[0]] += 1
        rolls.append(roll())
        while rolls[-1] != 7 and rolls[-1] != rolls[0]:
            rolls.append(roll())
        if rolls[-1] == 7:
            win = False
        else:
            win = True
            magic_win_count[rolls[0]] += 1

    # Record data
    if win:
        total_win_count += 1

    roll_count_distribution[len(rolls)] += 1

    # Print log of gameplay
    if print_output:
        print(",".join([str(x) for x in rolls]) +
              " - " + ("Win" if win else "Loss"))

# Print results
print("-----------------")

print(str(total_game_count) + " total games")
print(str(total_win_count) + " total wins")
print()
print(str(sum(magic_game_count.values())) + " \"magic\" games")
print(str(sum(magic_win_count.values())) + " \"magic\" wins")

print("\nMagic win distribution:")
for i in [4, 5, 6, 8, 9, 10]:
    print("Roll " + str(i).zfill(2) + " - " +
          str(magic_win_count[i]) + "/" + str(magic_game_count[i]))

print("\nRoll count distribution:")
for i in list(range(len(roll_count_distribution)))[::-1]:
    if roll_count_distribution[i] > 0:
        longest_roll = i
        break
for i in range(longest_roll + 1):
    print(str(i).zfill(2) + " rolls - " +
          str(roll_count_distribution[i]))
