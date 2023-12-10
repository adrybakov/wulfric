import wulfric as wulf

l = wulf.lattice_example("CUB")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("cub_real.png")
# Interactive plot:
backend.show()
