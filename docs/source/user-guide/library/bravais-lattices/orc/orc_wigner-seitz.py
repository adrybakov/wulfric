import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orc_wigner-seitz.png")
# Interactive plot:
backend.show()
