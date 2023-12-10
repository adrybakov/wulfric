import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCL")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mcl_wigner-seitz.png")
# Interactive plot:
backend.show()
