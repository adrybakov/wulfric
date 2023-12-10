import wulfric as wulf

l = wulf.lattice_example("ORCF3")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("orcf3_wigner-seitz.png")
# Interactive plot:
backend.show()
