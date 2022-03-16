if (rimfax == "ikke"):
	aktivering(aktivere="aktiverer", tool="rimfax")

if (spektrometer == "ikke"):
	aktivering(aktivere="aktiverer", tool="spektormeter")

if (rover == "i"):
	for i in range( 5 ):
		lagre_data(lagre="minne")
		forsinkelser("30m")
	
	aktivering(aktivere="deaktiverer", tool="spektormeter")
	aktivering(aktivere="deaktiverer", tool="rimfax")

