import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("BCT1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("bct1_wigner-seitz.png")
# Interactive plot:
backend.show()
