import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("RHL2")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("rhl2_brillouin.png")
# Interactive plot:
backend.show()
