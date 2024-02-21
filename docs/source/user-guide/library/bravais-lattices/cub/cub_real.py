import wulfric as wulf

l = wulf.lattice_example("{name}")
# Standardization is explicit since 0.3
l.standardize()
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("cub_real.png")
# Interactive plot:
backend.show()
