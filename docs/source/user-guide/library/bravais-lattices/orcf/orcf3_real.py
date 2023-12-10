import wulfric as wulf

l = wulf.lattice_example("ORCF3")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("orcf3_real.png")
# Interactive plot:
backend.show()
