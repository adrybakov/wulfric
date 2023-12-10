import wulfric as wulf

l = wulf.lattice_example("RHL2")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("rhl2_real.png")
# Interactive plot:
backend.show()
