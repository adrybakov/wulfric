import wulfric as wulf

l = wulf.lattice_example("TET")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("tet_wigner-seitz.png")
# Interactive plot:
backend.show()
