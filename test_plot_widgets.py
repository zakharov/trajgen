import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import process
import test_blend
from copy import copy


def plot(input):
    traj = test_blend.calc_traj(input)
    traj, seg_time, vel_extremum = test_blend.interpolate_traj(input.n_dof, traj, 0.1)

    # Create the figure and the line that we will manipulate
    lines_vel = []
    lines_acc = []
    fig, ax = plt.subplots()
    for t in traj:
        line, = plt.plot(t.t_sum, t.v, lw=2)
        lines_vel.append(line)
        line, = plt.plot(t.t_sum, t.a, lw=2, linestyle='--')
        lines_acc.append(line)

    ax.set_xlabel('Time [s]')
    axlines = []
    labels = []
    for st in seg_time:
        axline = plt.axvline(st, linestyle='--')
        axlines.append(axline)
        label_seg = plt.text(0.85 * st / traj[0].t_sum[-1], -0.4, f'seg: {st:.3f}', transform=ax.transAxes)
        labels.append(label_seg)

    label_tsum = plt.text(0.85, -0.4, f'total: {traj[0].t_sum[-1]:.3f}', transform=ax.transAxes)

    vel_sliders = []

    pos = 0.1
    for dof in range(input.n_dof):
        for i in range(len(seg_time)):
            pos = pos + 0.1 * i / 2.0
            vel_slider = Slider(
                ax=plt.axes([0.25, pos, 0.65, 0.03]),
                label=f'Exit vel dof: {dof} seg: {i}',
                valmin=-input.max_velocity[0],
                valmax=input.max_velocity[0],
                valinit=0,
            )
            vel_slider.on_changed(lambda x, dof=dof, i=i: update(x, dof, i))
            vel_sliders.append(vel_slider)

        pos = pos + 0.05

    def update(val, dof, index):
        input.target_velocity[index][dof] = val
        input.current_velocity[index + 1][dof] = val
        traj = test_blend.calc_traj(input)

        counter = 0
        # for t in range(len(traj)-1):
        #     str = f"seg: {counter} "
        #     for i in range(traj[t].degrees_of_freedom):
        #         str = str + f"dof{i}: v = {traj[t].profiles[0][i].v[4]}, a = {traj[t].profiles[0][i].a[6]} "
        #
        #
        #     print(str)
        #     counter = counter + 1

        traj, seg_time, vel_extremum = test_blend.interpolate_traj(input.n_dof, traj, 0.1)

        for i in range(len(lines_vel)):
            lines_vel[i].set_xdata(traj[i].t_sum)
            lines_vel[i].set_ydata(traj[i].v)
            lines_acc[i].set_xdata(traj[i].t_sum)
            lines_acc[i].set_ydata(traj[i].a)

        for i in range(len(seg_time)):
            axlines[i].set_xdata(seg_time[i])
            labels[i].set_text(f'seg: {seg_time[i]:.3f}')
            labels[i].set_x(0.85 * seg_time[i] / traj[0].t_sum[-1])

        label_tsum.set_text(f'{traj[0].t_sum[-1]:.3f}')

        fig.canvas.draw_idle()

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.1, bottom=pos + 0.15)

    # The function to be called anytime a slider's value changes

    # register the update function with each slider
    # vel_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    reset_button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        for f in vel_sliders:
            f.reset()

    reset_button.on_clicked(reset)

    calcax = plt.axes([0.65, 0.025, 0.1, 0.04])
    calc_button = Button(calcax, 'Calculate', hovercolor='0.975')

    def sign(val):
        return math.copysign(1.0, val)

    def calculate(event):
        traj = test_blend.calc_traj(input)
        counter = 0

        counter = 0

        for i in range(traj[0].degrees_of_freedom):
            for t in range(len(traj) - 1):
                if sign(traj[t].profiles[0][i].v[4]) == sign(traj[t + 1].profiles[0][i].v[4]):
                    val = min(traj[t].profiles[0][i].v[4], traj[t + 1].profiles[0][i].v[4])
                    vel_sliders[counter].set_val(val)
                    print(val)
                counter = counter + 1
                # str = str + f"dof{i}: v = {}, a = {traj[t].profiles[0][i].a[6]} "

        # for dof in range(input.n_dof):
        #     val = 0
        #     for i in range(len(vel_extremum) - 1):
        #         val = min(vel_extremum[i][dof], vel_extremum[i + 1][dof])
        #         vel_sliders[counter].set_val(val)
        #         counter = counter + 1

        # vel_sliders[counter].set_val(val)
        # vel_sliders[counter + 1].set_val(val)
        # counter = counter + 1

    calc_button.on_clicked(calculate)

    plt.show()


if __name__ == '__main__':
    inp = process.Input(3, [0, 0, 0], [[1.0, 2, 4], [-3, 5, 4]], [10, 20, 10], [1, 1, 1], [0.5, 0.5, 0.5], [1, 1, 1],
                        [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    plot(inp)
