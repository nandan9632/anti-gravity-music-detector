import matplotlib.pyplot as plt
import numpy as np

def show_floating_text(text):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    t = ax.text(5, 5, text, fontsize=20, ha='center')

    for i in range(40):
        y = 5 + np.sin(i / 2)
        t.set_position((5, y))
        plt.pause(0.1)

    plt.close()