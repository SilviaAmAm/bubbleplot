import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import seaborn as sns
sns.set()
sns.set_style("white")
sns.set_context("poster")

from bubbleplot import positions

# Obtain the positions of the new centres
radii = tuple(range(1,30))
centres = positions.spawn_bubbles(radii)
new_centres = positions.foptimise_positions(radii, centres, n_steps=5000, learning_rate=0.0005)

# Plot the bubble chart
fig, ax = plt.subplots(figsize=(7,7))
ax.set_axis_off()
radii = np.asarray(radii)
circ_list = []
for i in range(len(radii)):
    circ = Ellipse((new_centres[i,0], new_centres[i,1]), width=radii[i]*2, height=radii[i]*2, alpha=0.5)
    circ_list.append(circ)
    ax.add_patch(circ)
ax.set_xlim((min(new_centres[:,0])-max(radii),max(new_centres[:,0])+max(radii)))
ax.set_ylim((min(new_centres[:,1])-max(radii),max(new_centres[:,1])+max(radii)))
plt.show()