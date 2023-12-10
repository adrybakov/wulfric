import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCLC5")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc5_wigner-seitz.png")
# Interactive plot:
backend.show()
