from pathlib import Path
from sys import path
import process
from matplotlib import pyplot as plt

# Path to the build directory including a file similar to 'ruckig.cpython-37m-x86_64-linux-gnu'.
build_path = Path(__file__).parent.absolute().parent / 'build'
path.insert(0, str(build_path))

from ruckig import InputParameter, Ruckig, Trajectory, Result, Synchronization

if __name__ == '__main__':
    n_dof = 3
    inp = InputParameter(n_dof)

    inp.current_position = [0.0, 0.0, 0.0]
    inp.current_velocity = [0.0, 0, 0]
    inp.current_acceleration = [0.0, 0, 0]

    inp.target_position = [5, 2, 10]
    inp.target_velocity = [0.0, 0, 0]
    inp.target_acceleration = [0.0, 0.0, 0.0]

    inp.max_velocity = [3.0, 1.0, 3.0]
    inp.max_acceleration = [3.0, 2.0, 1.0]
    inp.max_jerk = [4.0, 3.0, 2.0]

    # Set different constraints for negative direction
    inp.min_velocity = [-1.0, -0.5, -3.0]
    inp.min_acceleration = [-2.0, -1.0, -2.0]

    inp.synchronization = Synchronization.Phase

    # We don't need to pass the control rate (cycle time) when using only offline features
    otg = Ruckig(n_dof)
    trajectory = Trajectory(n_dof)

    # Calculate the trajectory in an offline manner
    result = otg.calculate(inp, trajectory)
    if result == Result.ErrorInvalidInput:
        raise Exception('Invalid input!')

    print(f'Trajectory duration: {trajectory.duration:0.4f} [s]')

    new_time = 1.0
    t = 0;
    dt = 0.1
    traj = [process.Trajectory([], [], [], [], []) for _ in range(n_dof)]
    while t < trajectory.duration:
        # Then, we can calculate the kinematic state at a given time
        new_position, new_velocity, new_acceleration = trajectory.at_time(t)
        for i in range(len(new_position)):
            traj[i].t_sum.append(t)
            traj[i].t.append(dt)
            traj[i].p.append(new_position[i])
            traj[i].v.append(new_velocity[i])
            traj[i].a.append(new_acceleration[i])
        print(f'Position at time {t:0.4f} [s]: {new_position}')
        t = t + dt

    print(traj)
    plt.plot(traj[0].t_sum, traj[0].a)
    plt.plot(traj[0].t_sum, traj[0].v)
    plt.plot(traj[1].t_sum, traj[1].a)
    plt.plot(traj[1].t_sum, traj[1].v)
    plt.plot(traj[2].t_sum, traj[2].a)
    plt.plot(traj[2].t_sum, traj[2].v)
    plt.show()
    # # Then, we can calculate the kinematic state at a given time
    # new_position, new_velocity, new_acceleration = trajectory.at_time(new_time)
    #
    # print(f'Position at time {new_time:0.4f} [s]: {new_position}')
    #
    # # Get some info about the position extrema of the trajectory
    # print(f'Position extremas are {trajectory.position_extrema}')
