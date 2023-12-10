import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI1b")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tri1b_brillouin.png")
# Interactive plot:
backend.show()
