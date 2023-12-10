import wulfric as wulf

l = wulf.lattice_example("ORC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("orc_real.png")
# Interactive plot:
backend.show()
