import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orc_brillouin.png")
# Interactive plot:
backend.show()
