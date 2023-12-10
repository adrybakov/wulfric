import wulfric as wulf

l = wulf.lattice_example("TRI2a")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tri2a_wigner-seitz.png")
# Interactive plot:
backend.show()
