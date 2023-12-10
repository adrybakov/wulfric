import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("CUB")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("cub_brillouin.png")
# Interactive plot:
backend.show()
