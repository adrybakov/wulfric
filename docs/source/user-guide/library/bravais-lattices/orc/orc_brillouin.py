import wulfric as wulf

l = wulf.lattice_example("ORC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("orc_brillouin.png")
# Interactive plot:
backend.show()
