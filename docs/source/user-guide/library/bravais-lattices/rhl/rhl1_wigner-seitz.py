import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("RHL1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("rhl1_wigner-seitz.png")
# Interactive plot:
backend.show()
