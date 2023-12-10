import wulfric as wulf

l = wulf.lattice_example("RHL1")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("rhl1_real.png")
# Interactive plot:
backend.show()
