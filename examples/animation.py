import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Ellipse
import numpy as np

from bubbleplot import positions

def update(frame, trajectory, circ_list, radii, ax):

    for i in range(len(radii)):
        centre = trajectory[frame]
        circ = circ_list[i]
        circ.set_center((centre[i,0], centre[i,1]))

    return ax,

def get_animation(radii, centres, return_traj=True, n_steps=5000, learning_rate=0.0005, rep_const=600):

    new_centers, trajectory = positions.optimise_positions(radii, centres, return_traj=return_traj, n_steps=n_steps,
                                                           learning_rate=learning_rate, rep_const=rep_const)

    radii = np.asarray(radii)
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_axis_off()
    circ_list = []
    for i in range(len(radii)):
        circ = Ellipse((centres[i,0], centres[i,1]), width=radii[i]*2, height=radii[i]*2, alpha=0.5)
        circ_list.append(circ)
        ax.add_patch(circ)
    # ax.set_xlim((min(centres[:,0]),max(centres[:,0])))
    # ax.set_ylim((min(centres[:,0]),max(centres[:,0])))
    ax.set_xlim((min(centres[:, 0]) - max(radii), max(centres[:, 0]) + max(radii)))
    ax.set_ylim((min(centres[:, 1]) - max(radii), max(centres[:, 1]) + max(radii)))

    frames = list(range(0, len(trajectory), 20))
    ani = animation.FuncAnimation(fig, update, frames, init_func=None, blit=False, interval=1,
                                  fargs=(trajectory, circ_list, radii, ax))

    ## To save the animation uncomment this bit. If it doesnt work, you may need to add the path to the ffmpeg binary
    ## plt.rcParams['animation.ffmpeg_path'] = '/path/to/bin/ffmpeg'
    # writer = animation.FFMpegWriter(fps=30, bitrate=1800)
    # ani.save(filename='bubbles.mp4', writer=writer, dpi=100)

    plt.show()

if __name__ == "__main__":

    radii = tuple(range(1,30))
    centres = positions.spawn_bubbles(radii)

    get_animation(radii, centres, return_traj=True, n_steps=7000, learning_rate=0.000005, rep_const=2000)
