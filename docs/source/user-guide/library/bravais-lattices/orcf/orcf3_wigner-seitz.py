import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCF3")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orcf3_wigner-seitz.png")
# Interactive plot:
backend.show()
