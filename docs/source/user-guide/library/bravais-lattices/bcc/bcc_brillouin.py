import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("BCC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("bcc_brillouin.png")
# Interactive plot:
backend.show()
