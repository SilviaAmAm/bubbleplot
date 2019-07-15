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

def optimise_positions(radii, centres, return_traj=False):
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
    n_steps = 5000

    # Give random velocities to the particles
    # current_velocities = np.random.rand(n_bubbles, 2)
    current_velocities = np.zeros((n_bubbles,2))

    # Calculate the forces acting on the particles
    current_forces = get_vdw_forces(radii, centres)

    # Integrate equations of motion
    current_positions = centres
    if return_traj:
        traj_log = [current_positions]

    for i in range(n_steps):
        new_positions = update_positions(current_positions, current_velocities, current_forces, 0.01)
        new_forces = get_vdw_forces(radii, new_positions)
        new_velocities = update_velocities(current_velocities, current_forces, new_forces, 0.01)

        current_positions = new_positions
        current_velocities = new_velocities
        current_forces = new_forces

        if return_traj:
            traj_log.append(current_positions)

    if return_traj:
        return current_positions, np.asarray(traj_log)
    else:
        return current_positions

def get_vdw_forces(radii, centres):
    """
    Calculates the Van der Waals force acting on each particle. The parameters are pulled out
    of thin air by yours truly.

    :return: force
    """
    n_bubbles = len(radii)
    forces = np.zeros((n_bubbles, 2))

    for i in range(n_bubbles-1):
        for j in range(i+1, n_bubbles):
            dist_vec = (centres[j]-centres[i])/np.linalg.norm((centres[j]-centres[i]))    # unit vector from i to j
            force_mag = get_vdw_force_magnitude(radii[i], radii[j], centres[i], centres[j])
            forces[i] += dist_vec * force_mag
            forces[j] += -1 * dist_vec * force_mag

    return forces

def get_vdw_force_magnitude(r1,r2, centre1, centre2):
    """
    Takes in the radii of 2 particles and returns the magnitude of the force acting between them.

    :param r1: radius of particle 1
    :param r2: radius of particle 2
    :param centre1: centre of particle 1
    :param centre2: centre of particle 2
    :return: force magnitude
    """
    dist_vec = centre2-centre1
    dist = np.linalg.norm(dist_vec)

    # The minimum of the potential: just over the sum of the two radii
    a = r1 + r2 + 1

    pair_force = 2*(dist-a)*dist

    return pair_force

def update_positions(current_positions, current_velocities, current_forces, time_step=0.001):
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
    new_positions = current_positions + current_velocities * time_step + 0.5 * current_forces * (time_step ** 2)
    return new_positions

def update_velocities(current_velocities, current_forces, new_forces, time_step=0.001):
    """
    Updates the velocities using the velocity verlet algorithm

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

    new_velocities = current_velocities + (current_forces + new_forces)*0.5*time_step
    new_velocities = new_velocities/np.linalg.norm(new_velocities, axis=0)
    return new_velocities