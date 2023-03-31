from main import gen_board, simulate
import matplotlib.pyplot as plt
import time

def game_sim():
    counts, rolls = [], []
    reps = 1_000_000

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

    # scatter plots of all values do not provide helpful information

    # iteration = list(range(len(data)))

    # # plot dict of all values
    # plt.figure(fig_num)
    # for name in all_vals:  
    #     # to generate separate plots:  
    #     # plt.figure(fig_num+[k for k in all_vals].index(name))
    #     plt.scatter(iteration, all_vals[name], label=name)
    #     plt.ylabel("Number of times X was generated")
    #     plt.xlabel("X")
    #     plt.title("Frequency of generating X")
    #     plt.legend()

    # create dict mapping keys to average values
    avg_vals = {}

    for elt in all_vals:
        avg_vals[elt] = sum(all_vals[elt]) / len(all_vals[elt])

    # print out results
    for elt in avg_vals:
        print(f"{elt} was generated {avg_vals[elt]} times on average")
    print()

    # plot dict of average values
    plt.figure(fig_num*10+fig_num)
    plt.bar([k for k in avg_vals], [avg_vals[k] for k in avg_vals])
    plt.ylabel("Average number of times X was generated")
    plt.xlabel("X")
    plt.title("Average frequency of generating X")


def main():
    start_time = time.time()

    counts, rolls = game_sim()
    plot(counts, 1)
    plot(rolls, 2)

    print("--- %s seconds ---" % (time.time() - start_time))

    plt.show()


if __name__ == "__main__":
    main()