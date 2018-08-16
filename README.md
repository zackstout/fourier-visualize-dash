
# Fourier Visualization
Encoding a visualization of the Fourier transform to enrich my inuitions about it.

## Built With
- Dash
- Python

## Animation
![](https://media.giphy.com/media/lzJ7oEGGwM09GYQo2B/giphy.gif)

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
- Dash has a nice `code_container` style.

## Notes on Fourier:
- Dot product provides measure of similarity between two waves.
- Its magnitude tells us "how much" that certain sine wave is present in the original signal.
- Need to *also* compute dot product with cosine waves so as not to miss anything.
- We can then interpret these values as coordinates in the complex plane.
- So the phasor magnitude (its radius) corresponds to its strength, and the rate at which line moves around it corresponds to its frequency.
