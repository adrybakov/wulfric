import wulfric as wulf

l = wulf.lattice_example("MCLC3")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc3_real.png")
# Interactive plot:
backend.show()
