import wulfric as wulf

l = wulf.lattice_example("MCLC3")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mclc3_brillouin.png")
# Interactive plot:
backend.show()
