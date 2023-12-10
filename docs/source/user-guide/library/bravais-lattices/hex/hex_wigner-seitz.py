import wulfric as wulf

l = wulf.lattice_example("HEX")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("hex_wigner-seitz.png")
# Interactive plot:
backend.show()
