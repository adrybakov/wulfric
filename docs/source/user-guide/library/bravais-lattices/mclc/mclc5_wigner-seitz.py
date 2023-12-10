import wulfric as wulf

l = wulf.lattice_example("MCLC5")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc5_wigner-seitz.png")
# Interactive plot:
backend.show()
