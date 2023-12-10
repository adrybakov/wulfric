import wulfric as wulf

l = wulf.lattice_example("MCLC5")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mclc5_brillouin.png")
# Interactive plot:
backend.show()
