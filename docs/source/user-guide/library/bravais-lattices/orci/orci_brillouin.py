import wulfric as wulf

l = wulf.lattice_example("ORCI")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orci_brillouin.png")
# Interactive plot:
backend.show()
