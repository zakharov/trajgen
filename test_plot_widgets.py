import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import process
import test_blend
from copy import copy


# The parametrized function to be plotted
def f(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)


def plot(input):
    print(input)
    traj = test_blend.calc_traj(input)
    print(traj)
    traj, seg_time = test_blend.interpolate_traj(input.n_dof, traj, 0.1)

    # Create the figure and the line that we will manipulate
    lines = []
    fig, ax = plt.subplots()
    for t in traj:
        line, = plt.plot(t.t_sum, t.v, lw=2)
        lines.append(line)

    for st in seg_time:
        plt.axvline(st, linestyle='--')

    ax.set_xlabel('Time [s]')

    pos = 0.1
    freq_sliders = []

    def update(val, index):
        print(input)
        print(f"{index}: {val}")
        input.target_velocity[index][0] = val
        input.current_velocity[index + 1][0] = val
        print(input)
        traj = test_blend.calc_traj(input)

        traj, seg_time = test_blend.interpolate_traj(input.n_dof, traj, 0.1)
        for i in range(len(lines)):
            lines[i].set_xdata(traj[i].t_sum)
            lines[i].set_ydata(traj[i].v)

        fig.canvas.draw_idle()

    for i in range(len(seg_time)):
        print(i)
        pos = pos + 0.1 * i / 2.0
        freq_slider = Slider(
            ax=plt.axes([0.25, pos, 0.65, 0.03]),
            label=f'Exit velocity seg {i}',
            valmin=-input.max_velocity[0],
            valmax=input.max_velocity[0],
            valinit=0,
        )
        freq_slider.on_changed(lambda x, i=i: update(x, i))
        freq_sliders.append(freq_slider)

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.1, bottom=pos + 0.15)

    # The function to be called anytime a slider's value changes

    # register the update function with each slider
    # freq_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        for f in freq_sliders:
            f.reset()

    button.on_clicked(reset)

    plt.show()


if __name__ == '__main__':
    inp = process.Input(3, [0, 0, 0], [[1, 2, 3], [2, 2, 4]], [10, 10, 10], [1, 1, 1], [1, 1, 1], [1, 1, 1],
                        [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    plot(inp)
