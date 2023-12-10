import wulfric as wulf

l = wulf.lattice_example("TRI1a")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tri1a_real.png")
# Interactive plot:
backend.show()
