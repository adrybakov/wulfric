import wulfric as wulf

l = wulf.lattice_example("MCLC4")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc4_wigner-seitz.png")
# Interactive plot:
backend.show()
