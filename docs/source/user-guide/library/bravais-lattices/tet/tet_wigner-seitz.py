import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TET")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tet_wigner-seitz.png")
# Interactive plot:
backend.show()
