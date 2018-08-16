
# Fourier Visualization
Encoding a visualization of the Fourier transform to enrich my intuitions about it.

## Built With
- Dash
- Python

## Animation
![](https://media.giphy.com/media/lzJ7oEGGwM09GYQo2B/giphy.gif)

## Next Steps
- [ ] Create a button that adds new input fields, each of whose inputs controls a new line on the graph (or perhaps creates a new graph, re-spacing the graphs on the DOM?).
- [ ] Represent each sine wave as a phasor (a vector spinning round in a circle).
- [x] Give these phasors the correct size, and concatenate them into a larger spirograph, and show how this relates to the original sum graph. (See [this repo](https://github.com/zackstout/fourier-canvas))

## Notes on Fourier:
- Dot product provides measure of similarity between two waves.
- Its magnitude tells us "how much" that certain sine wave is present in the original signal.
- Need to *also* compute dot product with cosine waves so as not to miss anything.
- We can then interpret these values as coordinates in the complex plane.
- So the phasor magnitude (its radius) corresponds to its strength, and the rate at which line moves around it corresponds to its frequency.
- Why does the Fourier Transform always produce harmonically related phasors? (Each spins at a speed which is a multiple of the first's speed)

## Notes
- Dash has a nice `code_container` style.
