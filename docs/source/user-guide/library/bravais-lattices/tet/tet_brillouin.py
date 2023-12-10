import wulfric as wulf

l = wulf.lattice_example("TET")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tet_brillouin.png")
# Interactive plot:
backend.show()
