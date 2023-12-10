import wulfric as wulf

l = wulf.lattice_example("BCT1")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("bct1_brillouin.png")
# Interactive plot:
backend.show()
