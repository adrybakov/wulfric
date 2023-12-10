import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI1a")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tri1a_real.png")
# Interactive plot:
backend.show()
