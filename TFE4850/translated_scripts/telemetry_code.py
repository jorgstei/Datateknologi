for i in range( 10 ):
	if (satellitt != "funnet"):
		sok_etter_satelitt(azimuth="30", elevation="45", signalstyrke="-60db")
		sok_etter_satelitt(azimuth="60", elevation="90", signalstyrke="-70db")
		sok_etter_satelitt(azimuth="120", elevation="60", signalstyrke="-80db")
	
	forsinkelse("1")

if (satellitt == "funnet"):
	if (ingenioralgoritme == "kjort"):
		telemetripakke("ingenior fra disk")
		telemetripakke("ingenior til minne")
		send_pakke(gruppe="ingenior", frekvens="x-band")
	
	if (fysikeralgoritme == "kjort"):
		telemetripakke("fysiker fra disk")
		telemetripakke("fysiker til minne")
		send_pakke(gruppe="fysiker", frekvens="x-band")
	
	if (marsgeologalgoritme == "kjort"):
		telemetripakke("marsgeolog fra disk")
		telemetripakke("marsgeolog til minne")
		send_pakke(gruppe="marsgeolog", frekvens="x-band")
	

		