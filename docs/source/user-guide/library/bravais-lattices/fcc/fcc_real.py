import wulfric as wulf

l = wulf.lattice_example("FCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("fcc_real.png")
# Interactive plot:
backend.show()
