import multiprocessing as mp
import random
import math


# Roll two dice and get the sum
def roll():
    return random.randint(1, 6) + random.randint(1, 6)


# Play a series of games and return the results
def play_series(game_count, queue):
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
        rolls = [roll()]
        if rolls[0] == 7 or rolls[0] == 11:
            win = True
        elif rolls[0] == 2 or rolls[0] == 3 or rolls[0] == 12:
            win = False
        else:
            results["magic_game_count"][rolls[0]] += 1
            rolls.append(roll())
            while rolls[-1] != 7 and rolls[-1] != rolls[0]:
                rolls.append(roll())
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

    # Return final results
    queue.put(results)


# Main code
if __name__ == "__main__":
    total_game_count = int(input("How many games? "))

    # Divide games between threads
    core_count = mp.cpu_count()
    thread_count = core_count * 4
    print("Using " + str(thread_count) +
          " threads (" + str(core_count) + " cores detected)")
    thread_game_counts = [
        math.floor(total_game_count / thread_count)] * thread_count
    remaining_game_count = total_game_count - sum(thread_game_counts)
    for i in range(remaining_game_count):
        thread_game_counts[i] += 1

    # Start threads
    queue = mp.Queue()  # Queue for returning results from each thread
    for i in range(thread_count):
        process = mp.Process(target=play_series,
                             args=(thread_game_counts[i], queue))
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

        total_win_count += result["total_win_count"]
        for magic, count in result["magic_game_count"].items():
            magic_game_count[magic] += count
        for magic, count in result["magic_win_count"].items():
            magic_win_count[magic] += count
        for f in range(len(result["roll_count_distribution"])):
            if len(roll_count_distribution) <= f:
                roll_count_distribution.append(0)
            roll_count_distribution[f] += result["roll_count_distribution"][f]

    # Print results
    print("-------------------------")

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
