import wulfric as wulf

l = wulf.lattice_example("MCL")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("mcl_real.png")
# Interactive plot:
backend.show()
