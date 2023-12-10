import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("RHL1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("rhl1_real.png")
# Interactive plot:
backend.show()
