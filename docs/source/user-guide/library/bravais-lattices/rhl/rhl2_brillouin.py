import wulfric as wulf

l = wulf.lattice_example("RHL2")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("rhl2_brillouin.png")
# Interactive plot:
backend.show()
