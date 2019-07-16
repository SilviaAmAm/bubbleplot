import numpy as np

def get_centres(radii):
    """
    This function takes in a tuple of radii and returns a numpy array of 2D coordinates for the centres of the bubbles.

    :param radii: Radii of the bubbles
    :type radii: tuple of size (N,)
    :return: the coordinates of the bubbles
    :rtype: numpy array of shape (N,2)
    """

    # Assign random non-overlapping positions
    initial_centres = spawn_bubbles(radii)

    # Move particles according to minimise energy of the system
    final_centres = optimise_positions(radii, initial_centres)

def spawn_bubbles(radii):
    """
    This function spawns the bubbles in initial non-overlapping positions. It uses a grid, where the distance between
    the points is twice the largest radius.

    :param radii: Radii of the bubbles
    :type radii: tuple of size (N,)
    :return: the coordinates of the bubbles
    :rtype: numpy array of shape (N,2)
    """

    n_bubbles = len(radii)

    # Define the number of positions on the side of the square grid
    length = int(n_bubbles/2)+1
    n_grid_points = length**2

    # Give an index along the grid to every point
    indices = np.linspace(0,n_grid_points, num=n_grid_points+1)
    np.random.shuffle(indices)
    indices = indices[:n_bubbles]

    # Find the coordinates of every point
    coordinates = np.zeros((n_bubbles,2))

    for i in range(n_bubbles):
        index1 = int(indices[i] / length)
        index2 = indices[i] % length

        coordinates[i][0] = index1 * 2*max(radii)
        coordinates[i][1] = index2 * 2*max(radii)

    return np.asarray(coordinates)

def optimise_positions(radii, centres, return_traj=False, n_steps=5000, learning_rate=0.001):
    """
    This function takes in positions and centres and moves the positions so that the bubbles are close to each other.

    :param radii: Radii of the bubbles
    :type radii: tuple of size (N,)
    :param centres: the coordinates of the bubbles
    :type centres: numpy array of shape (N,2)
    :return: final coordinates of the bubbles
    :rtype: numpy array of shape (N,2)
    """
    n_bubbles = len(radii)

    # Calculate the forces acting on the particles
    current_forces = get_forces(radii, centres)

    # Optimisation
    current_positions = centres
    if return_traj:
        traj_log = [current_positions]

    for i in range(n_steps):
        new_positions = update_positions(current_positions, current_forces, learning_rate)
        new_forces = get_forces(radii, new_positions)

        current_positions = new_positions
        current_forces = new_forces

        if return_traj:
            traj_log.append(current_positions)

    if return_traj:
        return current_positions, np.asarray(traj_log)
    else:
        return current_positions

def foptimise_positions(radii, centres, n_steps=5000, learning_rate=0.001):
    """
    This function takes in positions and centres and moves the positions so that the bubbles are close to each other.
    It uses fortran so its faster.

    :param radii: Radii of the bubbles
    :type radii: tuple of size (N,)
    :param centres: the coordinates of the bubbles
    :type centres: numpy array of shape (N,2)
    :return: final coordinates of the bubbles
    :rtype: numpy array of shape (N,2)
    """

    from bubbleplot import foptimise

    n_bubbles = len(radii)
    radii = np.asarray(radii)

    final_positions = foptimise.optimise_pos(radii, centres, n_steps, learning_rate, n_bubbles)
    return final_positions

def get_forces(radii, centres):
    """
    Calculates the harmonic force acting on each particle.

    :param radii: Radii of the bubbles
    :type radii: tuple of size (N,)
    :param centres: the coordinates of the bubbles
    :type centres: numpy array of shape (N,2)
    :return: forces on the bubbles
    :rtype: numpy array of shape (N,2)
    """
    n_bubbles = len(radii)
    forces = np.zeros((n_bubbles, 2))

    for i in range(n_bubbles-1):
        for j in range(i+1, n_bubbles):
            dist_vec = (centres[j]-centres[i])/np.linalg.norm((centres[j]-centres[i]))    # unit vector from i to j
            force_mag = get_force_magnitude(radii[i], radii[j], centres[i], centres[j])
            forces[i] += -1 * dist_vec * force_mag
            forces[j] += dist_vec * force_mag

    return forces

def get_force_magnitude(r1, r2, centre1, centre2):
    """
    Takes in the radii of 2 particles and returns the magnitude of the force acting between them.

    :param r1: radius of particle 1
    :param r2: radius of particle 2
    :param centre1: centre of particle 1
    :type centre1: np array of shape (2,)
    :param centre2: centre of particle 2
    :type centre2: np array of shape (2,)
    :return: force magnitude
    """
    dist_vec = centre2-centre1
    dist = np.linalg.norm(dist_vec)-r1-r2

    # The minimum of the potential: just over the sum of the two radii
    if dist < 0:
        pair_force = 600*dist
    else:
        pair_force = 2*dist

    return pair_force

def update_positions(current_positions, current_forces, time_step=0.001):
    """
    Updates the position using the velocity verlet algorithm

    :param current_positions: position of the particles
    :type current_positions: numpy array of shape (N, 2)
    :param current_velocities: velocity of the particles
    :type current_velocities: numpy array of shape (N, 2)
    :param current_forces: forces acting on the particles
    :type current_forces: numpy array of shape (N, 2)
    :param time_step: time step for the integrator
    :return: new positions
    :rtype: numpy array of shape (N, 2)
    """
    new_positions = current_positions - time_step * current_forces
    return new_positions
