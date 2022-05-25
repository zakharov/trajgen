from process import process
from request import request
from matplotlib import pyplot as plt
from numpy import interp


def test(request_filename, url):
    traj_json = request(request_filename, url)
    traj, seg = process(traj_json)
    print(seg)
    
    dt = 0.001
    tt = [[traj[0].t_sum[0]], [traj[1].t_sum[0]]]
    a = [[traj[0].a[0]], [traj[1].a[0]]]
    v = [[traj[0].v[0]], [traj[1].v[0]]]
    p = [[traj[0].p[0]], [traj[1].p[0]]]
    te = max(traj[0].t_sum[-1], traj[1].t_sum[-1])
    for i in range(0,2):
        n = 0;
        t = 0;
        while t < te:
            n = n + 1
            t = t + dt
            # Then, we can calculate the kinematic state at a given time
            new_acceleration = interp(t, traj[i].t_sum, traj[i].a)
            new_velocity = v[i][n-1] + new_acceleration * dt;
            new_position = p[i][n-1] + new_velocity * dt;
            tt[i].append(t)
            a[i].append(new_acceleration)
            v[i].append(new_velocity)
            p[i].append(new_position)    
    
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    
    ax1.plot(tt[0], p[0])
    ax1.plot(tt[1], p[1])
    ax2.plot(tt[0], v[0])
    ax2.plot(tt[1], v[1])
    ax3.plot(tt[0], a[0])
    ax3.plot(tt[1], a[1])
    for dof in seg:
        for t in dof:
            ax1.axvline(x=t, linestyle='--')
            ax2.axvline(x=t, linestyle='--')
            ax3.axvline(x=t, linestyle='--')
    plt.show()


if __name__ == '__main__':
    test('test1.json', 'http://api.ruckig.com/calculate')
