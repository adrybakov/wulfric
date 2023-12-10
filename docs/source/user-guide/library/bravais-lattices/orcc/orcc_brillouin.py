import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orcc_brillouin.png")
# Interactive plot:
backend.show()
