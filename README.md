
# Fourier Visualization
Encoding a visualization of the Fourier transform to enrich my inuitions about it.

## Built With
- Dash
- Python

## Hopefuls
- [ ] Create a button that adds new input fields, each of whose inputs controls a new line on the graph (or perhaps creates a new graph, re-spacing the graphs on the DOM?).
- [ ] Sum up the sine waves to create a new sine wave.
- [ ] Represent each sine wave as a phasor (a vector spinning round in a circle).
- [ ] Give these phasors the correct size, and concatenate them into a larger spirograph.
- [ ] Show how this relates to the original sum-graph.

- [ ] Do we have to change amplitude ever? I think two sliders for each wave: a shifter and a dilater. Only the dilating factor will affect the phasor.
- I'm thinking we *do* have to care about amplitude: that controls the size of the phasor disc.

- Why does the Fourier Transform always produce harmonically related phasors? (Each spins at a speed which is a multiple of the first's speed)

- If this is the case, maybe we *don't* need amplitude: we just have frequency of the wave controlling the size of its phasor. No, that seems wrong -- frequency needs to match up to spinning-time.
