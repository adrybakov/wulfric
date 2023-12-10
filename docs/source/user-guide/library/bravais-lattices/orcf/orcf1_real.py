import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("ORCF1")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("orcf1_real.png")
# Interactive plot:
backend.show()
