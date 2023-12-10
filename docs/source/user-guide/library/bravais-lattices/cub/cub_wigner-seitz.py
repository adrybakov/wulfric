import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("CUB")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("cub_wigner-seitz.png")
# Interactive plot:
backend.show()
