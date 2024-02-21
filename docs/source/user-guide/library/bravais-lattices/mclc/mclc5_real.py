import wulfric as wulf

l = wulf.lattice_example("{name}")
# Standardization is explicit since 0.3
l.standardize()
backend = wulf.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("mclc5_real.png")
# Interactive plot:
backend.show()
