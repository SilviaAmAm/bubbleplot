import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from bubbleplot import positions

def update(frame, scat_plot, trajectory):
    scat_plot.set_offsets(trajectory[frame])

    return scat_plot,


def get_animation(radii, centres):

    new_centers, trajectory = positions.optimise_positions(radii, centres, return_traj=True)

    radii = np.asarray(radii)
    fig = plt.figure(figsize=(10,10))
    scat = plt.scatter(centres[:,0], centres[:,1], s=radii, alpha=0.5)

    frames = list(range(0, len(trajectory), 1))
    ani = animation.FuncAnimation(fig, update, frames, init_func=None, blit=False, interval=1,
                                  fargs=(scat, trajectory))

    plt.show()

if __name__ == "__main__":
    # radii = (1, 1)
    # centres = np.array([[-1, 0], [1, 0]])

    radii = (4.5, 5.0, 1.1, 0.6, 3.5)
    centres = positions.spawn_bubbles(radii)

    get_animation(radii, centres)