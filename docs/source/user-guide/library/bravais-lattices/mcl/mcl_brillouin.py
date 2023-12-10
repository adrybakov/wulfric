import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCL")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mcl_brillouin.png")
# Interactive plot:
backend.show()
