import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TRI2a")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tri2a_real.png")
# Interactive plot:
backend.show()
