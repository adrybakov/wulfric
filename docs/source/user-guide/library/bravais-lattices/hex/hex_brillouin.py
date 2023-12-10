import wulfric as wulf

l = wulf.lattice_example("HEX")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("hex_brillouin.png")
# Interactive plot:
backend.show()
