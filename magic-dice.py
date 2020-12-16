import multiprocessing as mp
import random
import time
import math

# Storing all possible rolls greatly improves performance
normal_rolls = [2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7,
                7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12]
trick_rolls = [2, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7,
               7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 12]


# Roll two dice and get the sum
def roll(trick_die):
    return random.choice(trick_rolls if trick_die else normal_rolls)


# Play a series of games and return the results
def play_series(game_count, trick_die, print_output, queue):
    results = {
        "total_win_count": 0,
        "magic_game_count": {
            4: 0,
            5: 0,
            6: 0,
            8: 0,
            9: 0,
            10: 0
        },
        "magic_win_count": {
            4: 0,
            5: 0,
            6: 0,
            8: 0,
            9: 0,
            10: 0,
        },
        "roll_count_distribution": []
    }

    # Loop through each game
    for i in range(game_count):
        # Play the game!
        rolls = [roll(trick_die)]
        if rolls[0] == 7 or rolls[0] == 11:
            win = True
        elif rolls[0] == 2 or rolls[0] == 3 or rolls[0] == 12:
            win = False
        else:
            results["magic_game_count"][rolls[0]] += 1
            rolls.append(roll(trick_die))
            while rolls[-1] != 7 and rolls[-1] != rolls[0]:
                rolls.append(roll(trick_die))
            if rolls[-1] == 7:
                win = False
            else:
                win = True
                results["magic_win_count"][rolls[0]] += 1

        # Record win
        if win:
            results["total_win_count"] += 1

        # Record roll count
        while len(results["roll_count_distribution"]) <= len(rolls):
            results["roll_count_distribution"].append(0)
        results["roll_count_distribution"][len(rolls)] += 1

        # Print log of game
        if print_output:
            print(",".join([str(x) for x in rolls]) +
                  " - " + ("W" if win else "L"))

    # Return final results
    queue.put(results)


# Main code
if __name__ == "__main__":
    # Detect core count
    thread_count = mp.cpu_count()
    print(str(thread_count) + " cores detected")

    # Get settings
    total_game_count = int(input("How many games? "))
    trick_die = input("Use trick die? ") == "y"
    print_output = input("Print output? (slower) ") == "y"

    # Divide games between threads
    thread_game_counts = [
        math.floor(total_game_count / thread_count)] * thread_count
    remaining_game_count = total_game_count - sum(thread_game_counts)
    for i in range(remaining_game_count):
        thread_game_counts[i] += 1

    # Start threads
    queue = mp.Queue()  # Queue for returning results from each thread
    start_time = time.time()
    for i in range(thread_count):
        process = mp.Process(target=play_series,
                             args=(thread_game_counts[i], trick_die, print_output, queue))
        process.start()

    # Record results
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
    roll_count_distribution = []
    for i in range(thread_count):
        result = queue.get()

        # Compile results from all threads
        total_win_count += result["total_win_count"]
        for magic, count in result["magic_game_count"].items():
            magic_game_count[magic] += count
        for magic, count in result["magic_win_count"].items():
            magic_win_count[magic] += count
        for f in range(len(result["roll_count_distribution"])):
            if len(roll_count_distribution) <= f:
                roll_count_distribution.append(0)
            roll_count_distribution[f] += result["roll_count_distribution"][f]
    end_time = time.time()

    # Print results
    print("-------------------------")
    print("Finished in " +
          str(round((end_time - start_time) * 1000) / 1000) + " seconds")
    print(("Trick" if trick_die else "Normal") + " die")
    print()
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
    for i in range(1, len(roll_count_distribution)):
        print(str(i).zfill(2) + " rolls - " + str(roll_count_distribution[i]))
