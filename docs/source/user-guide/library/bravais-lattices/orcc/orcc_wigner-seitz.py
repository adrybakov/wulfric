import wulfric as wulf

l = wulf.lattice_example("ORCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orcc_wigner-seitz.png")
# Interactive plot:
backend.show()
