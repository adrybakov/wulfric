import wulfric as wulf

l = wulf.lattice_example("HEX")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("hex_real.png")
# Interactive plot:
backend.show()
