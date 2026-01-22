import matplotlib.pyplot as plt

def plot_curve(x, y, xlabel, ylabel, title, label):
    plt.plot(x, y, marker="o", label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
