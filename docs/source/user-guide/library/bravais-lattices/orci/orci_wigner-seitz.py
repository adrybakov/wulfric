import wulfric as wulf

l = wulf.lattice_example("ORCI")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orci_wigner-seitz.png")
# Interactive plot:
backend.show()
