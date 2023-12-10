import wulfric as wulf

l = wulf.lattice_example("TRI1a")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tri1a_brillouin.png")
# Interactive plot:
backend.show()
