import wulfric as wulf

l = wulf.lattice_example("TRI1b")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tri1b_real.png")
# Interactive plot:
backend.show()
