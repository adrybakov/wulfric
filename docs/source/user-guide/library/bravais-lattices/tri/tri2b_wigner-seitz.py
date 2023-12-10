import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI2b")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tri2b_wigner-seitz.png")
# Interactive plot:
backend.show()
