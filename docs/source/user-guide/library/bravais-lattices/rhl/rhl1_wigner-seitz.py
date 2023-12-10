import wulfric as wulf

l = wulf.lattice_example("RHL1")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("rhl1_wigner-seitz.png")
# Interactive plot:
backend.show()
