import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("HEX")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("hex_wigner-seitz.png")
# Interactive plot:
backend.show()
