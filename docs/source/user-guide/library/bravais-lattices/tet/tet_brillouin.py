import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TET")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tet_brillouin.png")
# Interactive plot:
backend.show()
