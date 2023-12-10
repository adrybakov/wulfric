import wulfric as wulf

l = wulf.lattice_example("BCT1")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("bct1_real.png")
# Interactive plot:
backend.show()
