import wulfric as wulf

l = wulf.lattice_example("TRI2b")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tri2b_wigner-seitz.png")
# Interactive plot:
backend.show()
