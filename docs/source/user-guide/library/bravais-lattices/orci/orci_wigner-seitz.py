import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCI")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orci_wigner-seitz.png")
# Interactive plot:
backend.show()
