import wulfric as wulf

l = wulf.lattice_example("RHL1")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("rhl1_brillouin.png")
# Interactive plot:
backend.show()
