import wulfric as wulf

l = wulf.lattice_example("TRI1b")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tri1b_wigner-seitz.png")
# Interactive plot:
backend.show()
