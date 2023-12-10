import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORC")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("orc_real.png")
# Interactive plot:
backend.show()
