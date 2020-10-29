#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape


def normalize(s):
    s = s.lower()
    replacements = (
        ("á", "A"),
        ("é", "E"),
        ("í", "I"),
        ("ó", "O"),
        ("ú", "U"),
        ("ñ", "N")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    
    return s



def application(environ, start_response):
    status = '200 OK'    
    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])
    texto_normalizado = normalize(texto)
    text =transcribe(texto_normalizado)
    
    #preparing response
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [text]



def transcribe(oracion):
	medida = len(oracion)
	#different indicators
	esp=0
	n = 0
	voc = 0
	rasgo= 0
	#subsiguiente vocal
	vsigg=""
	transcripcion ="" 

	while (n < medida):
		 
		c = oracion[n]
		impres ="" 	#qué imprimimos en pantalla
		vsig=""
		
		if (n < medida-1):	 #si no es el ultimo caracter
			vsig = oracion[n+1] #letra siguiente
		
		if (n > 0):	 #si no es el primer caracter
			vant = oracion[n-1] #letra anterior


		if (vsig==" "):
			esps = 1
		elif not (vsig == " "):
			esps = 0
		
		if (vsigg == " " or vsig == " " ):
			vsigg = oracion[n+3] 
		

		if (vsig == " "):
			vsig = oracion[n+2]

		if ( (vsig == "h") and (not (c == "c")) ):
			vsig = vsigg
		
		
		if (c == "." or c == "," or c == ";"):
			impres= ""
			rasgo = 0 


		if (c == " "):
			impres=" "
			esp = 1
			
			
		if (c == "a"):
			impres=  "a"
			rasgo = "vocal"
			voc = "a"
			esp = 0
		
			
		if (c == "A"):
			impres=  "a"
			rasgo = "vocal"
			voc = "a"
			esp = 0
			
		if (c == "E"):
			impres=  "e";
			rasgo = "vocal";
			voc = "e";
			esp = 0; 
			
		if (c == "I"):
			impres=  "i"
			rasgo = "vocal"
			voc = "ii"
			
		if (c == "O"):
			impres=  "o"
			rasgo = "vocal"
			voc = "o"
			esp = 0

		if (c == "U"):
			impres=  "u"
			rasgo = "vocal"
			voc = "uu"
						
			
		#resto de letras
		if (c == "b"):
			if (rasgo == "vocal" or rasgo == "l" or rasgo == "r"):
				
				#si la siguiente vocal es vocal o liquida, entonces la b es aproximante
				if ( re.findall("[aeiouáéíóúrl]", vsig) ):
					impres="β" 
				else:
					impres=  "b"
			else:
				impres=  "b"

			rasgo = "b"
			

		if (c == "c"):
			if ( vsig =="h" ):
				impres="tʃ"
				n=n+1
				rasgo = "tS" 
			elif ( vsig == "e" or vsig == "i" or vsig == "í" ):
				impres="θ"
				rasgo ="Z" 
			else:
				impres=  "k"
				rasgo = "k"
		

		if (c == "d"):
			if ( (rasgo == "vocal") or (rasgo == "r")):
				if (re.findall("[aeiouáéíóúrl]", vsig)):
					impres=  "ð"	
				else:
					impres=  "d"
			else:
				impres=  "d"
			rasgo= "d";
	

		if (c == "e"):
			impres=  "e"
			rasgo = "vocal"
			voc = "e"
			esp = 0 

	
		if (c == "f"):
			impres=  "f"
			rasgo = "f"



		if (c == "g"):
			if (vsig == "a" or vsig == "á"):
				if ( (rasgo == "vocal") or (rasgo == "s") or (rasgo == "r") or (rasgo == "l")):
					impres=  "ɣ̞"
				else:
					impres=  "g"
			elif (vsig == "ü"):
				if ( (rasgo == "vocal") or (rasgo == "s") or (rasgo == "r") or (rasgo == "l") ):
					impres="ɣ̞w"
				else:
					impres= "gw"
				n=n+1;
			
			elif (vsig == "e" or vsig == "é" ):
				impres=  "x"
		
			elif (vsig == "i" or vsig == "í"):
				impres=  "x"
		
			elif (vsig == "o" or vsig == "ó"):
				if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
					impres=  "ɣ̞"
				else:
					impres=  "g"

			elif (vsig == "u" or vsig == "ú"):

				if ( vsigg == "e" or vsigg == "i" or vsigg == "í" or  vsigg == "é"):
					n= n+1
					if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
						impres="ɣ̞"
					else:
						impres=  "g"			
				else:
					if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
						impres="ɣ̞"
					else:
						impres=  "g"
			
			
			elif (vsig == "r" or vsig == "l"):
				if (rasgo == "vocal"):
					impres="ɣ̞"
					rasgo = "G"
				else:
					impres= "g" 
					rasgo = "g"
		
			else:
				impres=  "g"
				rasgo = "g"


		#if (c == "h"):
			#do nothing

		if (c == "i"):
			if ( (rasgo == "vocal") or (re.findall("[aeiouáéíóú]", vsig)) ):
				if (not (re.findall(" ",vant))):
					impres=  "j"
					rasgo = "vocal"
					voc = "ï"
			else:
				impres=  "i" 
				rasgo = "vocal"
				voc = "i"
			if (re.findall(" ", vant)):
				impres= "i"
				esp = 0


		if (c == "j"):
				impres= "x"
				rasgo= "x"


		if (c == "k"):
				impres= "k"
				rasgo = "k"


		if (c == "l"):
			if ( (vsig == "l") and ( not vsigg == "l") and  ( not esps == 1)):
				if (rasgo == "vocal"):
					impres=  "ʎ"
				elif (not rasgo == "vocal"):
					impres=  "ʎ"
				n= n+1
			

			elif ( (vsig == "l") and (not vsigg == "l") and (esps == 1) ):
				impres=  "l l"
				n = n+2;
				esps = 0
		

			elif (vsig == "l" and vsigg == "l" and esps == 1):
				impres=  "ʎ ʎ";
				n = n+3;
				esps = 0;
			
			else:
				impres=  "l"
				rasgo = "l"
				esp = 0
				rasgo = "l"


		if (c == "m"):
				if (vsig == "f"):
					impres=  "M"
				else:
					impres=  "m"
				rasgo = "m"
		
		if (c == "n"):
			if (vsig == "t" or vsig == "d" or vsig == "z"):
				impres=  "n̟" 

			elif ((vsig == "c" or vsig == "q") and (vsigg == "a" or vsigg == "o" or vsigg == "u")):
				impres="ŋ"

			elif (vsig == "b" or vsig == "v" or vsig == "p" or vsig == "m"):
				impres=  "m"
			
			elif (vsig == "g" or vsig == "j"):
				impres="ŋ"
				
			elif (vsig == "f"):
				impres=  "ɱ"
				
			elif ((vsig == "c") and (vsigg == "e" or vsigg == "i")):
				impres=  "n̟"	
			
			elif ( ( (vsig == "y") and (re.findall ("[aeiou]",vsigg))) or (vsig == "l" and vsigg == "l") ):
				impres=  "ɲ"
			else:
				impres=  "n"
	
			rasgo = "n";


		if (c == "N"):
			impres=  "ɲ"
			rasgo ="N"
		
		
		if (c == "o"):
			impres=  "o"
			rasgo = "vocal"
			voc = "o"
			esp = 0

		if (c == "p"):
			impres=  "p"
			rasgo = "p"
			
		if (c == "q"):
			impres=  "k"
			n=n+1
			rasgo = "q"


		if (c == "r"):
			if (rasgo == "t" or rasgo == "d" or rasgo == "p" or rasgo == "b" or rasgo == "k" or rasgo == "g" or rasgo == "G" or rasgo == "f"):
				impres="r"
				rasgo = "r"
			
			elif (vsig == "r"):
				rasgo = "r"
			
			elif ( (not vsig == "r") and rasgo == "r" and ( not esp == 1)):
				impres="ř"
				rasgo = "R"

			elif (rasgo == "vocal" and ( not vsig == "r")  and  (not esp == 1)):
				impres=  "r"
				rasgo = "r"
			
			elif ( not esp == 0):
				impres=  "ř"
				rasgo = "R"
			
			elif ( ( not esp == 1) and ( not rasgo == "R") ):
				impres=  "ř"
				rasgo = "R"
			
			elif ( (not esp == 1) and (not rasgo == "R")):
				impres=  "ř"
				rasgo ="R"
				esp= 0
			else:
				impres=  "*"
			
		


		if (c == "s"):
			if ( (re.findall ("[bvdlmn]", vsig )) or (vsig == "g" and ( (not vsigg == "e") and (not vsigg == "i"))) ): 
				impres=  "z"
				rasgo = "vocal"
			else:
				impres=  "s"
				rasgo = "s"
		


		if (c == "t"):
			impres=  "t"
			rasgo = "t"
		

		if (c == "u"):
			if (rasgo == "vocal" and  (not voc == "ï")):
				impres=  "w";
				rasgo = "vocal";
				voc = "w";
				
			elif (re.findall ("[aeouáéó]",vsig)): 
				impres=  "w"
		
			else: 
				impres=  "u"
				rasgo = "vocal"
				voc = "u"
				esp = 0



		if (c == "v"):
			if (rasgo == "vocal" or rasgo == "l" or rasgo == "r"):
				if (re.findall("[aeiouáéíóúrl]",vsig)): 
					impres="β̞" 
					rasgo ="B"
				else:
					impres=  "b"
				
			else:
				impres=  "b"
			rasgo = "b";

			
			
		if (c == "w"):
			impres=  "w";
			rasgo = "w";
			
		if (c == "x"):
			impres=  "ks"
			rasgo = "x" 


		if (c == "y"):
			if (re.findall ("[aeiouáéíóú]",vsig) and esps == 0):
				impres= "y"
				rasgo= "vocal"
				voc="ï"  

			elif (rasgo == "vocal" or esps == 1):
				if ((rasgo == "vocal")):
					impres=  "i"  #aproximante
					rasgo = "vocal"
					voc = "ï"
				else:
					impres=  "i"
					rasgo = "vocal"
					voc = "i"
			else:
				impres=  "y"     	  
				
			esps = 0;	  
			
				
			
		if (c == "z"):
				impres="θ"
				rasgo = "Z"

		if (not rasgo == "vocal"):
				voc = 0			
	
						
			
	



		n=n+1
		transcripcion = transcripcion+impres
	
	return transcripcion


