import wulfric as wulf

l = wulf.lattice_example("BCC")
backend = wulf.PlotlyBackend()
backend.plot(l, kind="wigner-seitz")
# Save an image:
backend.save("bcc_wigner-seitz.png")
# Interactive plot:
backend.show()
