import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("HEX")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("hex_brillouin.png")
# Interactive plot:
backend.show()
