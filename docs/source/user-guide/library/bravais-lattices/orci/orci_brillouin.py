import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCI")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orci_brillouin.png")
# Interactive plot:
backend.show()
