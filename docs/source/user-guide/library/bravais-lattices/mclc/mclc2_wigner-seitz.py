import wulfric as wulf

l = wulf.lattice_example("MCLC2")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc2_wigner-seitz.png")
# Interactive plot:
backend.show()
