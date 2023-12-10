import wulfric as wulf

l = wulf.lattice_example("FCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("fcc_brillouin.png")
# Interactive plot:
backend.show()
