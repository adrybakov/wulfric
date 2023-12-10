import wulfric as wulf

l = wulf.lattice_example("CUB")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("cub_wigner-seitz.png")
# Interactive plot:
backend.show()
