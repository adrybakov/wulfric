import wulfric as wulf

l = wulf.lattice_example("MCL")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mcl_wigner-seitz.png")
# Interactive plot:
backend.show()
