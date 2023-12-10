import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("CUB")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("cub_real.png")
# Interactive plot:
backend.show()
