import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("BCT1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("bct1_brillouin.png")
# Interactive plot:
backend.show()
