import wulfric as wulf

l = wulf.lattice_example("FCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("fcc_wigner-seitz.png")
# Interactive plot:
backend.show()
