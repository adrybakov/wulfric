import wulfric as wulf

l = wulf.lattice_example("MCLC2")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mclc2_brillouin.png")
# Interactive plot:
backend.show()
