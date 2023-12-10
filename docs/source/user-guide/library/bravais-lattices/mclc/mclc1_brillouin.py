import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCLC1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mclc1_brillouin.png")
# Interactive plot:
backend.show()
