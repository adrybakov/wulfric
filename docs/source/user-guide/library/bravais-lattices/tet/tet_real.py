import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("TET")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("tet_real.png")
# Interactive plot:
backend.show()
