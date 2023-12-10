import wulfric as wulf

l = wulf.lattice_example("ORCF2")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orcf2_brillouin.png")
# Interactive plot:
backend.show()
