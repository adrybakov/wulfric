import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("FCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("fcc_brillouin.png")
# Interactive plot:
backend.show()
