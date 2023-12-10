import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orcc_wigner-seitz.png")
# Interactive plot:
backend.show()
