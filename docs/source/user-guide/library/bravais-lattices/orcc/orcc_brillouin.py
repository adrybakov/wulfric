import wulfric as wulf

l = wulf.lattice_example("ORCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orcc_brillouin.png")
# Interactive plot:
backend.show()
