import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("RHL2")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("rhl2_real.png")
# Interactive plot:
backend.show()
