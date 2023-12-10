import wulfric as wulf

l = wulf.lattice_example("ORC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orc_wigner-seitz.png")
# Interactive plot:
backend.show()
