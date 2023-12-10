import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCF1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orcf1_brillouin.png")
# Interactive plot:
backend.show()
