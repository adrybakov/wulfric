import wulfric as wulf

l = wulf.lattice_example("{name}")
# Standardization is explicit since 0.3
l.standardize()
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("mclc3_wigner-seitz.png")
# Interactive plot:
backend.show()
