import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI1a")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tri1a_wigner-seitz.png")
# Interactive plot:
backend.show()
