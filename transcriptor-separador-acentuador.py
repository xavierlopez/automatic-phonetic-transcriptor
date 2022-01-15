#!/usr/bin/python36
# -*- coding: utf-8 -*-

import re
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import sys


def application(environ, start_response):
    status = '200 OK'
    origin = environ.get("HTTP_ORIGIN")
    
    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])
    # As there can be more than one value for a variable then
    # a list is provided as a default value.
    texto = d.get('texto', [''])[0] # Returns the first value
    
    texto_normalizado = normalize(texto)

    text_transcrito =transcribe(texto_normalizado)
    text_separado = acentuaysepara(text_transcrito)
    text = denormalize(text_separado)
 
    response_headers = [('Content-type', 'text/html;charset=utf-8'), ('Access-Control-Allow-Origin','*')]

    start_response(status, response_headers)
 
    return [text]



#input normalisation
def normalize(s):
    s = s.lower()
    replacements = (
        ("_", " "),
        ("á", "A"),
        ("é", "E"),
        ("í", "I"),
        ("ó", "O"),
        ("ú", "U"),
        ("ð", "D"),
        ("ñ", "9"),
        ("ü", "8"),        
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    print("*",s)
    return s



#output
def denormalize(s):
    replacements = (
        ("X", "tʃ"),
		("D", "ð"),
		("A","a"),
        ("E","e"),
        ("I","i"),
        ("O","o"),
        ("U","u"),
        ("D","ð"),
        ("G","ɣ"),
        ("L", "ʎ"),
        ("9", "ɲ"),
        ("R", "ř"),
        ("Z", "θ"),
	("M", "ɱ"),
        ("N", "ŋ"),
        ("B", "β"),
        ("9", "ɲ"),
        ("8", "ü")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    
    return s




def acentuaysepara(s):
	print ("input: ",s)
	grupo_vocal = "[aeiouAEIOU]"
	grupo_vocal2 = "[aeiouwjAEIOU]"
	grupo_semivocal = "[jw]"
	grupo_c1 = "[bBcdDfgGhklLmnñ9prRstvxXyzZ]"
	grupo_liquidas = "[nszrRñ9pkLmMlZNdDgb]"
	grupo_petaca = "[tkpgdDfbBG]"
	list_of_words=s.split(" ")
	
	#inicializamos frase_sil, que será una lista de palabras ya acentuadas
	frase_sil=[]
	
	for palabra in list_of_words:
		print ("palabra: ",palabra)
		pos = -1 #posicion por la derecha

		#declaramos word, que será una lista de silabas
		word =[]

		#iteramos por cada letra de la palabra
		while(len(palabra) >= abs(pos)):
			try:
				letra0 = palabra[pos]
			except:
  				letra0= "0"
			try:
				letra1 = palabra[pos-1]
			except:
  				letra1= "0"
			try:
				letra2 = palabra[pos-2]
			except:
  				letra2= "0"
			try:
				letra3 = palabra[pos-3]
			except:
  				letra3= "0"
			try:
				letra4 = palabra[pos-4]
			except:
  				letra4= "0"
			try:
				letra_sig = palabra[pos+1]
			except:
  				letra_sig= "0"
			silaba = "8xz"
			
			

			#caso CV
			if (re.search(letra0,grupo_vocal)):
				if (re.search(letra1,grupo_c1)):
					if not ( ((re.search(letra2,grupo_petaca)) and (re.findall(letra1,'[rl]'))) ):
						silaba = letra1+letra0
						pos=pos-1
						

			#caso CVC
			if (re.search(letra0,grupo_liquidas)):
				if (re.search(letra1,grupo_vocal)):
						if (re.search(letra2,grupo_c1)):
							if not ( (re.search(letra3,grupo_petaca) and (re.search(letra2,'[rl]'))) ):
								silaba = letra2+letra1+letra0
								pos= pos-2

			#caso V
			if (re.search(letra0,grupo_vocal)):
				if not (((re.search(letra1,grupo_c1)) or (re.search(letra1,grupo_semivocal)))):
					silaba = letra0


			#caso VC
			if ( (re.search(letra0,grupo_liquidas))   and   (re.search(letra1,grupo_vocal2))   ):
				if not (((re.search(letra2,grupo_c1)) or (re.search(letra2,grupo_semivocal)))):
					silaba = letra1+letra0
					pos=pos-1


			#caso VCC
			if ( (re.search(letra0,"[s]"))   and   (re.search(letra1,"[kn]")) and  (re.search(letra2,grupo_vocal))   ):
				silaba = letra2+letra1+letra0
				pos=pos-2

			#caso CCV
			if ( (re.search(letra0,grupo_vocal))   and   (re.search(letra1,"[rl]")) and  (re.search(letra2,grupo_petaca))   ):
				silaba = letra2+letra1+letra0
				pos=pos-2

			#caso CCVC
			if ( (re.search(letra0,grupo_liquidas))   and   (re.search(letra1,grupo_vocal)) and  (re.search(letra2,"[rl]")) and (re.search(letra3,grupo_petaca)) ):
				silaba = letra3+letra2+letra1+letra0
				pos=pos-3

			#caso CVCC
			if ( (re.search(letra0,"[s]"))   and   (re.search(letra1,"[b]")) and  (re.search(letra2,grupo_vocal)) and (re.search(letra3,"[s]")) ):
				silaba = letra3+letra2+letra1+letra0
				pos=pos-3


			#diftongos

			#caso CVv y Vv
			if ( (re.search(letra0,"[jw]")) and (re.search(letra1,"[aeiou]")) ):
				if ( re.search(letra2,grupo_c1) ):
					silaba = letra2+letra1+letra0
					pos = pos-2
				else:
					silaba = letra1+letra0
					pos = pos-1 


			#caso CvV
			if ( re.search(letra0,grupo_vocal) and (re.search(letra1,"[jw]")) ):
				if (re.search(letra2,grupo_c1)):
						silaba = letra2+letra1+letra0
						pos = pos-2
				elif ( re.search(letra0,"[aeiou]") and re.search(letra1,"[jw]")):
					silaba = letra1+letra0
					pos = pos-1


			#caso CvCV
			if ( (re.search(letra0,"[cksznNplrçm]"))  and  (re.search(letra1,grupo_vocal)) and (re.search(letra2,"[wj]"))  and  (re.search(letra3,grupo_c1))  ):
				silaba = letra3+letra2+letra1+letra0
				pos = pos-3

			#caso CCvV
			if ( (re.search(letra0,"[aeiou]"))  and  (re.search(letra1,"[jw]")) and  (re.search(letra2,"[rl]")) and  (re.search(letra3,grupo_petaca))  ):
				silaba = letra3+letra2+letra1+letra0
				pos = pos-3

			#caso CCVv
			if ( (re.search(letra0,"[jw]"))  and  (re.search(letra1,"[aeiou]")) and  (re.search(letra2,"[rl]")) and  (re.search(letra3,grupo_petaca))  ):
				silaba = letra3+letra2+letra1+letra0
				pos = pos-3


			#caso CCvVC
			if ( (re.search(letra0,"[cksznNplrçm]"))  and  (re.search(letra1,"[aeiou]")) and  (re.search(letra2,"[jw]")) and  (re.search(letra3,"[rl]")) and (re.search(letra2,grupo_petaca))  ):
				silaba = letra4+letra3+letra2+letra1+letra0
				pos = pos-4

			#### FIN DIPTONGOS



			#caso CCVCC
			if ( (re.search(letra0,"[s]"))  and  (re.search(letra1,"[n]")) and  (re.search(letra2,grupo_vocal)) and  (re.search(letra3,"[r]")) and (re.search(letra4,grupo_petaca))   ):
				silaba = letra4+letra3+letra2+letra1+letra0
				pos = pos-4

			#otros casos
			if ( (re.search(letra0,"[jw]")) ):
				if not ( (re.search(letra1,grupo_c1)) or (re.search(letra1,grupo_vocal)) ):
					silaba = letra0
				elif ((re.search(letra1,grupo_c1)) ):
					silaba=letra1+letra0
					pos = pos-1
			
			if (silaba=="8xz"):
				silaba = letra0


			word = ([silaba] + word)
			pos=pos-1	
		


		tonica_encontrada =0
		##asignamos acento si hay tónica
		i=0
		j=0
		while (j < len(word) ):
			if (re.findall(r'[A,E,I,O,U]',word[j])):
					word[j] = "'"+word[j]
					tonica_encontrada=1
					print("--------------------")
			j=j+1;

		if not (tonica_encontrada):

			while (i < len(word) ):	
				
				if (len(word) > 1 and (not tonica_encontrada)): #si no es monosilabbo
					if re.findall(r"[rlZdD]$", word[-1]):  #si la ultima silaba acaba en consonante
						word[-1]="'"+word[-1]
						tonica_encontrada=1	

					elif not (tonica_encontrada):
						word[-2]="'"+word[-2]
						tonica_encontrada=1					
				
				if ( len(word)==1 and re.findall("ir|ba|Ba",word[0]) ):
					word[0]="'"+word[0]
					tonica_encontrada=1
				elif (len(word)==1 and re.search(word[0],"[^']..+")): #si es monosilabo y tiene 3 o mas letras
					if not ( re.search(word[0],"^lo[sz]$|^la[sz]$") ): #excepto 'los' y 'las'
						word[0]="'"+word[0]
						tonica_encontrada=1

				i=i+1
		frase_sil = (frase_sil + word)
		frase_string = ' '.join( [str(elem) for elem in frase_sil] )
		
		tonica_encontrada =0
		word=[]
		
	return frase_string




def transcribe(oracion):
	medida = len(oracion)
	esp=0
	n = 0
	voc = 0
	rasgo= 0
	vsigg=""
	vant= " "
	transcripcion ="" 

	while (n < medida):
		 
		c = oracion[n]
		impres ="" 	#sonido por sonido
		vsig=""
		
		if (n < medida-1):	 #si no es el ultimo caracter
			vsig = oracion[n+1] #letra siguiente

		if (n < medida-2):	 #si no es el penultimo caracter
			vsigg = oracion[n+2]
		
		if (n > 0):	 #si no es el primer caracter
			vant = oracion[n-1] #letra anterior


		if (vsig==" "):
			esps = 1
			print ("hay espacio antes")

		elif not (vsig == " "):
			esps = 0
		
		if (vsigg == " " or vsig == " " ):
			try:
				vsigg = oracion[n+3] 
			except:
				print ("out of range in line 81")
		

		if (vsig == " "):
			try:
				vsig = oracion[n+2]
			except:
				print ("out of range in line 88")

		if ( (vsig == "h") and (not (c == "c")) ):
			vsig = vsigg
		
		
		if (c == "." or c == "," or c == ";"):
			impres= " "
			rasgo = 0 


		if (c == " "):
			impres=" "
				
			
		if (c == "a"):
			impres=  "a"
			rasgo = "vocal"
			voc = "a"
			esp = 0
		
			
		if (c == "A"):
			impres=  "A"
			rasgo = "vocal"
			voc = "a"
			esp = 0
			
		if (c == "E"):
			impres=  "E"
			rasgo = "vocal"
			voc = "e"
			esp = 0
			
		if (c == "I"):
			impres=  "I"
			rasgo = "vocal"
			voc = "ii"
			
		if (c == "O"):
			impres=  "O"
			rasgo = "vocal"
			voc = "o"
			esp = 0

		if (c == "U"):
			impres=  "U"
			rasgo = "vocal"
			voc = "uu"
						
			
		#resto de letras
		if (c == "b"):
			if (rasgo == "vocal" or rasgo == "l" or rasgo == "r"):
				
				#si la siguiente vocal es vocal o liquida, entonces la b es aproximante
				if ( re.findall("[aeiouAEIOUrl]", vsig) ):
					impres="B" 
				else:
					impres=  "b"
			else:
				impres=  "b"

			rasgo = "b"
			

		if (c == "c"):
			if ( vsig =="h" ):
				impres="X"
				n=n+1
				rasgo = "X" 
			elif ( vsig == "e" or vsig == "i" or vsig == "I" ):
				impres="Z"
				rasgo ="Z" 
			else:
				impres=  "k"
				rasgo = "k"
		

		if (c == "d"):
			if ( (rasgo == "vocal") or (rasgo == "r")):
				if (re.findall("[aeiouAEIOUrl]", vsig)):
					impres=  "D"	
				else:
					impres=  "d"
			else:
				impres=  "d"
			rasgo= "d"
	

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
					impres=  "G"
				else:
					impres=  "g"

			elif (vsig == "8"):
				if ( (rasgo == "vocal") or (rasgo == "s") or (rasgo == "r") or (rasgo == "l") ):
					impres="Gw"
				else:
					impres= "gw"
				n=n+1
			
			elif (vsig == "e" or vsig == "E" ):
				impres=  "x"
		
			elif (vsig == "i" or vsig == "I"):
				impres=  "x"
		
			elif (vsig == "o" or vsig == "O"):
				if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
					impres=  "G"
				else:
					impres=  "g"

			elif (vsig == "u" or vsig == "U"):
				
				if ( vsigg == "e" or vsigg == "i" or vsigg == "I" or  vsigg == "E"):
					n= n+1
					if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
						impres="G"	
					else:
						impres=  "g"			
				else:
						
					if (rasgo == "vocal" or rasgo == "s" or rasgo == "r" or rasgo == "l"):
						impres="G"
						rasgo="g"
					else:
						impres=  "g"
			
			
			elif (vsig == "r" or vsig == "l"):
				if (rasgo == "vocal"):
					impres="G"
					rasgo = "G"
				else:
					impres= "g" 
					rasgo = "g"
		
			else:
				impres=  "g"
				rasgo = "g"



		if (c == "i"):
			if ( (rasgo == "vocal") or (re.findall("[aeiouAEIOU]", vsig)) ):
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
			if ( (vsig == "l") and ( not vsigg == "l") and ( not esps == 1)):
				if (rasgo == "vocal"):
					impres=  "L"
				elif (not rasgo == "vocal"):
					impres=  "L"
				n= n+1
			

			elif ( (vsig == "l") and (not vsigg == "l")  ):
				impres=  "l l"
				n = n+2
				esps = 0
		

			elif (vsig == "l" and vsigg == "l"):
				impres=  "L"
				n = n+1
				esps = 0
			
			else:
				impres=  "l"
				rasgo = "l"
				esp = 0
				rasgo = "l"


		if (c == "m"):
				if (vsig == "f"):
					impres=  "ɱ"
				else:
					impres=  "m"
				rasgo = "m"
		
		if (c == "n"):
			if (vsig == "t" or vsig == "d" or vsig == "z"):
				impres=  "n" 

			elif ((vsig == "c" or vsig == "q") and (vsigg == "a" or vsigg == "o" or vsigg == "u")):
				impres="N"

			elif (vsig == "b" or vsig == "v" or vsig == "p" or vsig == "m"):
				impres=  "m"
			
			elif (vsig == "g" or vsig == "j"):
				impres="N"
				
			elif (vsig == "f"):
				impres=  "M"
				
			elif ((vsig == "c") and (vsigg == "e" or vsigg == "i")):
				impres=  "n"	
			
			elif ( ( (vsig == "y") and (re.findall ("[aeiou]",vsigg))) or (vsig == "l" and vsigg == "l") ):
				impres=  "9"
			else:
				impres=  "n"
	
			rasgo = "n"


		if (c == "9"):
			impres=  "9"
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
				impres="R"
				rasgo = "R"

			elif (rasgo == "vocal" and ( not vsig == "r")  and  (not esp == 1)):
				impres=  "r"
				rasgo = "r"
			
			elif ( not esp == 0):
				impres=  "R"
				rasgo = "R"
			
			elif ( ( not esp == 1) and ( not rasgo == "R") ):
				impres=  "R"
				rasgo = "R"
			
			elif ( (not esp == 1) and (not rasgo == "R")):
				impres=  "R"
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
				impres=  "w"
				rasgo = "vocal"
				voc = "w"
				
			elif (re.findall ("[aeouAEO]",vsig)): 
				impres=  "w"
		
			else: 
				impres=  "u"
				rasgo = "vocal"
				voc = "u"
				esp = 0



		if (c == "v"):
			if (rasgo == "vocal" or rasgo == "l" or rasgo == "r"):
				if (re.findall("[aeiouAEIOUrl]",vsig)): 
					impres="B" 
					rasgo ="B"
				else:
					impres=  "b"
				
			else:
				impres=  "b"
			rasgo = "b"

			
			
		if (c == "w"):
			impres=  "w"
			rasgo = "w"
			
		if (c == "x"):
			impres=  "ks"
			rasgo = "x" 


		if (c == "y"):
			if (re.findall ("[aeiouAEIOU]",vsig) and esps == 0):
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
				
			esps = 0
						
			
		if (c == "z"):
				impres="Z"
				rasgo = "Z"

		if (not rasgo == "vocal"):
				voc = 0			
	
						
		n=n+1
		transcripcion = transcripcion+impres
	
	return transcripcion
