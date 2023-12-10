import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("HEX")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("hex_real.png")
# Interactive plot:
backend.show()
