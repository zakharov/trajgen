from pathlib import Path
from sys import path
import process
import logging
from matplotlib import pyplot as plt
from copy import copy

from ruckig import InputParameter, Ruckig, Trajectory, Result, Synchronization

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def plot(traj, seg_time):
    for t in traj:
        plt.plot(t.t_sum, t.v)

    for st in seg_time:
        plt.axvline(st, linestyle='--')

    plt.show()


def interpolate_traj(n_dof, trajectory, dt):
    traj = [process.Trajectory([], [], [], [], []) for _ in range(n_dof)]
    global_time = 0
    seg_time = []
    for tr in trajectory:
        actual_time = 0
        while actual_time < tr.duration:
            pos, vel, acc = tr.at_time(actual_time)
            for i in range(tr.degrees_of_freedom):
                traj[i].t.append(dt)
                traj[i].t_sum.append(global_time)
                traj[i].p.append(pos[i])
                traj[i].v.append(vel[i])
                traj[i].a.append(acc[i])

            actual_time = actual_time + dt
            global_time = global_time + dt

        seg_time.append(global_time)

    if len(seg_time) > 1:
        del seg_time[-1]

    return traj, seg_time


def calc_segment(orig_traj_input, n_intermediate):
    traj_input = copy(orig_traj_input)
    otg = Ruckig(traj_input.n_dof)
    trajectory = Trajectory(traj_input.n_dof)
    if n_intermediate < 0:
        inp = create_ruckig_input(traj_input)
        otg.calculate(inp, trajectory)
    else:
        # first segment
        if n_intermediate == 0:
            logging.debug('First segment')
            traj_input.target_position = traj_input.intermediate_positions[0]
            inp = create_ruckig_input(traj_input)
            otg.calculate(inp, trajectory)
        # intermediate segment
        elif (n_intermediate > 0) and (n_intermediate < len(traj_input.intermediate_positions)):
            logging.debug('Intermediate segment')
            traj_input.current_position = traj_input.intermediate_positions[n_intermediate - 1]
            traj_input.target_position = traj_input.intermediate_positions[n_intermediate]
            inp = create_ruckig_input(traj_input)
            otg.calculate(inp, trajectory)
        # last segment
        else:
            logging.debug('Last segment')
            traj_input.current_position = traj_input.intermediate_positions[-1]
            inp = create_ruckig_input(traj_input)
            otg.calculate(inp, trajectory)

    return trajectory


def calc_traj(traj_input):
    traj = []
    if len(traj_input.intermediate_positions) == 0:
        traj.append(calc_segment(traj_input, -1))
    else:
        # intermediate
        for p in range(len(traj_input.intermediate_positions) + 1):
            traj.append(calc_segment(traj_input, p))

    return traj


def create_ruckig_input(input):
    inp = InputParameter(input.n_dof)
    inp.current_position = input.current_position
    inp.target_position = input.target_position
    inp.max_velocity = input.max_velocity
    inp.max_acceleration = input.max_acceleration
    inp.max_jerk = input.max_jerk
    return inp


if __name__ == '__main__':
    inp = process.Input(3, [0, 0, 0], [[1, 2, 3], [2, 2, 2]], [10, 10, 10], [1, 1, 1], [1, 1, 1], [1, 1, 1])
    traj = calc_traj(inp)
    # print(traj)
    traj, seg_time = interpolate_traj(3, traj, 0.1)
    plot(traj, seg_time)
