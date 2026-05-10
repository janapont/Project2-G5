import matplotlib.pyplot as plt
from . import statistics as stats


def plot_distribution(simulator):
    values, counts = stats.get_distribution(simulator)
    plt.figure()
    plt.bar(values, counts)
    plt.title("Distribution of Total Results")
    plt.xlabel("Result")
    plt.ylabel("Frequency")
    plt.grid(axis="y")
    plt.show()


def plot_single_dice(simulator):
    values, counts = stats.single_dice_distribution(simulator)
    plt.figure()
    plt.bar(values, counts)
    plt.title("Single Dice Distribution")
    plt.xlabel("Face")
    plt.ylabel("Frequency")
    plt.grid(axis="y")
    plt.show()


def plot_pairs_vs_odds(simulator):
    pairs = stats.percentage_of_pairs(simulator)
    odds = stats.percentage_of_odds(simulator)
    plt.figure()
    plt.bar(["Pairs (even)", "Odds"], [pairs, odds])
    plt.title("Pairs vs Odds")
    plt.ylabel("Percentage (%)")
    plt.grid(axis="y")
    plt.show()


def plot_doubles(simulator):
    if simulator.get_n_dice() == 1:
        return
    doubles = stats.percentage_of_doubles(simulator)
    non_doubles = 100 - doubles
    plt.figure()
    plt.bar(["Doubles", "Non-doubles"], [doubles, non_doubles])
    plt.title("Doubles vs Non-doubles")
    plt.ylabel("Percentage (%)")
    plt.grid(axis="y")
    plt.show()