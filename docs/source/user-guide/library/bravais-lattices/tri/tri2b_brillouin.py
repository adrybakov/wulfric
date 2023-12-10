import wulfric as wulf

l = wulf.lattice_example("TRI2b")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("tri2b_brillouin.png")
# Interactive plot:
backend.show()
