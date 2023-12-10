import wulfricshorttools as wulfricshort

l = wulfricshort.lattice_example("MCL")
backend = wulfricshort.PlotlyBackend()
backend.plot(l, kind="primitive")
# Save an image:
backend.save("mcl_real.png")
# Interactive plot:
backend.show()
