import wulfric as wulf

l = wulf.lattice_example("{name}")
# Standardization is explicit since 0.3
l.standardize()
backend = wulf.PlotlyBackend()
backend.plot(l, kind="brillouin-kpath")
# Save an image:
backend.save("mcl_brillouin.png")
# Interactive plot:
backend.show()
