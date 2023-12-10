import wulfric as wulf

l = wulf.lattice_example("ORCF3")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orcf3_brillouin.png")
# Interactive plot:
backend.show()
