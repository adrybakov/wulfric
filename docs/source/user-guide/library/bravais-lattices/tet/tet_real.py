import wulfric as wulf

l = wulf.lattice_example("TET")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tet_real.png")
# Interactive plot:
backend.show()
