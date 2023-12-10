import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("FCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("fcc_wigner-seitz.png")
# Interactive plot:
backend.show()
