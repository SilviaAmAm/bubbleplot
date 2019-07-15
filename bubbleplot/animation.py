import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Ellipse
import numpy as np

from bubbleplot import positions

# def update(frame, scat_plot, trajectory):
#     scat_plot.set_offsets(trajectory[frame])
#
#     return scat_plot,

def update(frame, trajectory, circ_list, radii, ax):

    for i in range(len(radii)):
        centre = trajectory[frame]
        circ = circ_list[i]
        circ.set_center((centre[i,0], centre[i,1]))

    return ax,


def get_animation(radii, centres, return_traj=True, n_steps=5000, learning_rate=0.0005):

    new_centers, trajectory = positions.optimise_positions(radii, centres, return_traj=return_traj, n_steps=n_steps, learning_rate=learning_rate)

    radii = np.asarray(radii)
    fig, ax = plt.subplots(figsize=(10,10))
    circ_list = []
    for i in range(len(radii)):
        circ = Ellipse((centres[i,0], centres[i,1]), width=radii[i]*2, height=radii[i]*2, alpha=0.5)
        circ_list.append(circ)
        ax.add_patch(circ)
    ax.set_xlim((min(centres[:,0]),max(centres[:,0])))
    ax.set_ylim((min(centres[:,0]),max(centres[:,0])))

    frames = list(range(0, len(trajectory), 1))
    ani = animation.FuncAnimation(fig, update, frames, init_func=None, blit=False, interval=1,
                                  fargs=(trajectory, circ_list, radii, ax))

    plt.show()

if __name__ == "__main__":
    # radii = (1, 1, 1)
    # centres = np.array([[-2, 0], [2, 0], [0,2]])

    radii = tuple(range(1,10))
    centres = positions.spawn_bubbles(radii)

    get_animation(radii, centres, return_traj=True, n_steps=5000, learning_rate=0.0005)