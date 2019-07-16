# Bubble plots

An optimiser that arranges bubbles in bubble charts. It takes in the radii of the circles and returns the positions of their centres.

![](https://github.com/SilviaAmAm/bubbleplot/blob/master/visuals/bubble.gif)

## How to use it

Clone this repository and pip install it:

```
git clone https://github.com/SilviaAmAm/bubbleplot.git
cd bubbleplot
pip install ./
```

Then, in a python script import it as:

```
from bubbleplot import positions
```

It takes a tuple of radii and a numpy array of x,y coordinates for the centres of the circles. It returns a numpy array of the optimised positions:

```
radii = (1, 1, 1)
centres = np.array([[-2, 0], [2, 0], [0,2]])
new_centres = positions.foptimise_positions(radii, centres, n_steps=5000, learning_rate=0.0005)
```

If you don't have initial positions for the centres, there is a function to spawn them:

```
centres = positions.spawn_bubbles(radii)
```

## Examples

In the [examples](./examples) folder, there is a [plot_bubble.py](./examples/plot_bubble.py) script that shows how to plot the bubbles and there is [animation.py](./examples/animation.py)  that shows how to make an animation of the optimisation process.