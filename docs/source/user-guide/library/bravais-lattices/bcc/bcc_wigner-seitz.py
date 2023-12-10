import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("BCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("bcc_wigner-seitz.png")
# Interactive plot:
backend.show()
