import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI1a")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tri1a_brillouin.png")
# Interactive plot:
backend.show()
