# TODO
# average game lasts 80 rounds
# add feature to generate new board after 80 rounds
# analyse average roll and resource distribution across all games

from main import gen_board, simulate
import matplotlib.pyplot as plt

def game_sim():
    counts, rolls = [], []
    reps = 1_000

    for _ in range(reps):
        board = gen_board()
        count, roll_freq = simulate(board, reps=80)
        counts.append(count)
        rolls.append(roll_freq)

    return counts, rolls


def plot(data, fig_num):
    # data is list of dictionaries

    # create dict mapping keys to list of all rolled values
    all_vals = {}
    
    for k in data[0]:
        all_vals[k] = []

    for elt in data:
        for k in elt:
            all_vals[k].append(elt[k])

    id_to_val = []
    for k in all_vals:
        id_to_val.append({i:all_vals[k][i] for i in all_vals[k]})

    # plot dict of all values
    plt.figure(fig_num)
    for i, elt in enumerate(id_to_val):  
        # to generate separate plots:  
        # plt.figure(fig_num+i)
        plt.scatter([k for k in elt], [elt[k] for k in elt], label=f"{[name for name in all_vals][i]}")
        plt.ylabel("Number of times X was generated")
        plt.xlabel("X")
        plt.title("Frequency of generating X")
        plt.legend()

    # create dict mapping keys to average values
    avg_vals = {}

    for elt in all_vals:
        avg_vals[elt] = sum(all_vals[elt]) / len(all_vals[elt])

    # plot dict of average values
    plt.figure(fig_num+10*fig_num)
    plt.bar([k for k in avg_vals], [avg_vals[k] for k in avg_vals])
    plt.ylabel("Average number of times X was generated")
    plt.xlabel("X")
    plt.title("Average frequency of generating X")


def main():
    counts, rolls = game_sim()
    plot(counts, 1)
    plot(rolls, 10)

    plt.show()


if __name__ == "__main__":
    main()