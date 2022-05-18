from dataclasses import dataclass


@dataclass
class Trajectory:
    t: []
    t_sum: []
    p: []
    v: []
    a: []


# Creating list of the trajectories with all the segments
# traj_json - trajectory in a json format obtained from the Ruckig
# Returns list of Trajectory
def process(traj_json):
    segment_id = 0
    n_dof = len(traj_json['independent_min_durations'])
    n_segments = len(traj_json['profiles'])
    traj = []
    seg_time = []
    for n in range(n_dof):
        traj.append(Trajectory([0], [0], [], [], []))  # push initial zero to the time
        seg_time.append([])

    for profile in traj_json['profiles']:
        dof_id = 0
        for dof in profile:
            seg_time[dof_id].append(dof['t_sum'][-1])
            traj[dof_id].p = traj[dof_id].p + dof['p']
            traj[dof_id].v = traj[dof_id].v + dof['v']
            traj[dof_id].a = traj[dof_id].a + dof['a']
            traj[dof_id].t = traj[dof_id].t + dof['t']
            if (segment_id + 1) < n_segments:
                del traj[dof_id].p[-1]
                del traj[dof_id].v[-1]
                del traj[dof_id].a[-1]
            # print(f"p: {len(dof['p'])}, v: {len(dof['a'])}, a: {len(dof['v'])}, t: {len(dof['t'])}")
            dof_id = dof_id + 1

        segment_id = segment_id + 1

    for tr in traj:
        for i in range(1, len(tr.t)):
            tr.t_sum.append(tr.t_sum[i - 1] + tr.t[i])

    for st in seg_time:
        for i in range(1, len(st)):
            st[i] = st[i - 1] + st[i]


    return traj, seg_time
