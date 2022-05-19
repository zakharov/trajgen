from process import process
from request import request
from matplotlib import pyplot as plt


def test(request_filename, url):
    traj_json = request(request_filename, url)
    traj, seg = process(traj_json)
    print(seg)
    plt.plot(traj[0].t_sum, traj[0].p)
    plt.plot(traj[1].t_sum, traj[1].p)
    plt.plot(traj[0].t_sum, traj[0].v)
    plt.plot(traj[1].t_sum, traj[1].v)
    for dof in seg:
        for t in dof:
            plt.axvline(x=t, linestyle='--')
    plt.show()


if __name__ == '__main__':
    test('test1.json', 'http://api.ruckig.com/calculate')
