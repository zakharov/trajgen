import json
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Trajectory:
    t: []
    t_sum: []
    p: []
    v: []
    a: []


def test(filename):
    with open(filename) as infile:
        data = json.load(infile)
        segment_id = 0
        n_dof = len(data['independent_min_durations'])
        n_segments = len(data['profiles'])
        traj = []
        fig = plt.figure()
        for n in range(n_dof):
            traj.append(Trajectory([0], [0], [], [], []))

        for profile in data['profiles']:
            dof_id = 0
            for dof in profile:
                traj[dof_id].p = traj[dof_id].p + dof['p']
                traj[dof_id].v = traj[dof_id].v + dof['v']
                traj[dof_id].a = traj[dof_id].a + dof['a']
                traj[dof_id].t = traj[dof_id].t + dof['t']
                if (segment_id + 1) < n_segments:
                    del traj[dof_id].p[-1]
                    del traj[dof_id].v[-1]
                    del traj[dof_id].a[-1]
                print(f"p: {len(dof['p'])}, v: {len(dof['a'])}, a: {len(dof['v'])}, t: {len(dof['t'])}")
                dof_id = dof_id + 1

            segment_id = segment_id + 1


        for tr in traj:
            for id in range(1, len(tr.t)):
                tr.t_sum.append(tr.t_sum[id - 1] + tr.t[id])

        print(f"p: {len(traj[0].p)}, v: {len(traj[0].a)}, a: {len(traj[0].v)}, t: {len(traj[0].t)}, t_sum: {len(traj[0].t_sum)}")
        plt.plot(traj[0].t_sum, traj[0].a)
        plt.plot(traj[1].t_sum, traj[1].a)
        plt.show()



if __name__ == '__main__':
    test('test_result.json')
