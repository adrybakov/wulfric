import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI1b")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tri1b_real.png")
# Interactive plot:
backend.show()
