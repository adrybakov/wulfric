import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCLC2")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc2_wigner-seitz.png")
# Interactive plot:
backend.show()
