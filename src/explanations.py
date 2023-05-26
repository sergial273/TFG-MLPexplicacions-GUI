import numpy as np
from keras.models import load_model
import chess
from stockfish import Stockfish

class Explanations:

	def __init__(self,stockfish):
			self.stockfish = Stockfish(path="./stockfish/stockfish-windows-2022-x86-64-avx2")

	def MLPexplanations(self, fen1, fen2):
			inputs = self.convertTuple((fen1,fen2))
			inputs = inputs.astype('float32') / 127
			model = load_model('./ModelFiles/model.h5')
			predictions = model.predict(inputs, verbose=0)
			return predictions[0]

	def MLPcolumns(self, fen1, fen2):
			inputs = self.convertTuple((fen1,fen2))
			inputs = inputs.astype('float32') / 127
			model = load_model('./ModelFiles/modelMLPcolumnes.h5')
			predictions = model.predict(inputs, verbose=0)
			return predictions[0]
	
	def restrictingMoves(self, fen1, fen2):
			board1 = chess.Board(fen1)
			board2 = chess.Board(fen2)
			
			board1.turn = board2.turn = chess.WHITE
			difW = len(list(board2.legal_moves))-len(list(board1.legal_moves))

			board1.turn = board2.turn = chess.BLACK
			difB = len(list(board2.legal_moves))-len(list(board1.legal_moves))

			return difW,difB

	def explanations(self, fen1, fen2):
			MLPexp = self.MLPexplanations(fen1,fen2)
			if np.sum(MLPexp[:10] == 1) > 1 and np.sum(MLPexp[:10] == 0) == len(MLPexp[:10]) - 1 and np.sum(MLPexp[:10] == 1) > 1 and np.sum(MLPexp[22:25] == 1) == 1:
				pass
			else:
				exp = self.calexplanations(fen1,fen2)
				exp = self.eval(exp[0],exp[2],fen1,fen2,exp[1])
				MLPexp = exp
			
			MLPcol = self.MLPcolumns(fen1,fen2)

			difW, difB = self.restrictingMoves(fen1, fen2)
			#agafar els primers 10 elements del array
			indices = np.where(MLPexp[:20] == 1)[0]
			if len(indices) == 1:
				ind = indices[0]
			else:
				ind = indices[1]
			
			dicEvals = {
				0:["[0, 0'25)",0],
				1:["[0'25, 0'5)",0],
				2:["[0'5, 0'75)",0],
				3:["[0'75, 1)",0],
				4:["[1, 1'25)",0],
				5:["[1'25, 1'5)",0],
				6:["[1'5, 2'5)",0],
				7:["[2'5, 3'5)",0],
				8:["[3'5, 4'5)",0],
				9:[" >= 4.5 ",0],
				10:["(0, -0'25)",1],
				11:["[-0'25, -0'5)",1],
				12:["[-0'5, -0'75)",1],
				13:["[-0'75, -1)",1],
				14:["[-1, -1'25)",1],
				15:["[-1'25, -1'5)",1],
				16:["[-1'5, -2'5)",1],
				17:["[-2'5, -3'5)",1],
				18:["[-3'5, -4'5)",1],
				19:[" <= -4.5 ",1],
			}
			
			eval = dicEvals[ind][0]
			
			mate = MLPexp[20]

			captura = MLPexp[21]

			escac = MLPexp[22]
			
			onmogut = MLPexp[23:26]

			if onmogut[0] == 1: onmogut = "centre"
			elif onmogut[1] == 1: onmogut = "mig"
			elif onmogut[2] == 1:
				onmogut = "exterior"

			control = MLPexp[26]

			if (fen1.split()[1] == "w" and dicEvals[ind][1] == 0) or (fen1.split()[1] == "b" and dicEvals[ind][1] == 1):
				frase_expl = "El moviment realitzat és favorable per tu. "

				if escac:
					frase_expl = frase_expl + "Has aturat l'escac"
					if captura:
						frase_expl = frase_expl + " i capturat una peça"
						if mate: frase_expl = frase_expl + ", però segueixes en mat."
						else: frase_expl = frase_expl + "."
					else:
						if mate: frase_expl = frase_expl + ", però segueixes en mat."
						else: frase_expl = frase_expl + "i millores la posició en general."

				else:
					if captura:
						frase_expl = frase_expl + " Has capturat una peça"
						if mate: frase_expl = frase_expl + ", però segueixes en mat."
						else: frase_expl = frase_expl + " i millorat la posició en general."
					else:
						if mate: frase_expl = frase_expl + "Tot i això, segueixes en mat."
						else: frase_expl = frase_expl + "En general, millores la posició."
						
			else:
				frase_expl = "El moviment realitzat és dolent per tu."

				if escac:
					frase_expl = frase_expl + "Tot i que has aturat l'escac"
					if captura:
						frase_expl = frase_expl + " i capturat una peça"
						if mate: frase_expl = frase_expl + "has facilitat el mat."
						else: frase_expl = frase_expl + "."
					else:
						if mate: frase_expl = frase_expl + ", facilites el mat."
						else: frase_expl = frase_expl + ", empitjores la posició en general."

				else:
					if captura:
						frase_expl = frase_expl + " Malgrat capturar una peça"
						if mate: frase_expl = frase_expl + ", facilites el mat."
						else: frase_expl = frase_expl + ", a vegades hi ha moviments millors."
					else:
						if mate: frase_expl = frase_expl + " Has facilitat el mat al rival."
						else: frase_expl = frase_expl + " En general, aquest moviment empitjora la teva posició."

			if onmogut != "exterior":
				frase_expl2 = "A part, la teva peça està ocupant el " + onmogut + ", "
			else:
				frase_expl2 = "A part, la teva peça està ocupant l'" + onmogut + ", "

			if (difW > 0 and difB>0) or (difW >= 0 and difB>0) or (difW > 0 and difB>=0):
				if difW > difB:
					if fen1.split()[1] == "w":
							if difB == 0:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior sense afectar els del rival. "
							else:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior i, en menor mesura, els del rival. "
					else:
						if difB == 0:
								frase_expl2 = frase_expl2 + "però, has augmentat els moviments possibles del rival respecte a la posició anterior sense afectar els teus. "
						else:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior, però, encara més els del teu rival. "
				elif difW < difB:
					if fen1.split()[1] == "w":
						if difW == 0:
								frase_expl2 = frase_expl2 + "però, has augmentat els moviments possibles del rival respecte a la posició anterior sense afectar els teus. "
						else:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior, però, encara més els del teu rival. "
					else:
						if difW == 0:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior sense afectar els del rival. "
						else:
								frase_expl2 = frase_expl2 + "a més, has augmentat els teus moviments possibles respecte a la posició anterior i, en menor mesura, els del rival. "
				elif difW == difB:
						frase_expl2 = frase_expl2 + "has augmentat els teus moviments, però també els del rival. "

			elif (difW < 0 and difB < 0) or (difW <= 0 and difB < 0) or (difW < 0 and difB <= 0):
				if difW > difB:
					if fen1.split()[1] == "w":
						if difW == 0:
							frase_expl2 = frase_expl2 + "a més, has restringit els moviments del teu rival. "
						else:
							frase_expl2 = frase_expl2 + "a més, tot i restringir els teus moviments, has restringit encara més els del rival. "
					else:
						if difW == 0:
							frase_expl2 = frase_expl2 + "però, has restringit els teus moviments, sense afectar els del rival. "
						else:
							frase_expl2 = frase_expl2 + "però, tot i restringir els moviments possibles del rival, has restringit encara més els teus. "

				elif difW < difB:
					if fen1.split()[1] == "w":
						if difB == 0:
							frase_expl2 = frase_expl2 + "però, has restringit els teus moviments, sense afectar els del rival. "
						else:
							frase_expl2 = frase_expl2 + "però, tot i restringir els moviments possibles del rival, has restringit encara més els teus. "
					else:
						if difB == 0:
							frase_expl2 = frase_expl2 + "a més, has restringit els moviments del teu rival. "
						else:
							frase_expl2 = frase_expl2 + "a més, tot i restringir els teus moviments, has restringit encara més els del rival. "
				elif difW == difB:
						frase_expl2 = frase_expl2 + "has restringit tant els teus moviments com els del rival d'igual manera. "

			elif (difW > 0 and difB < 0) or (difW >= 0 and difB < 0) or (difW > 0 and difB <= 0):
				if fen1.split()[1] == "w":
					if difW == 0:
						frase_expl2 = frase_expl2 + "a més, has aconseguit restringir els moviments del rival. "
					elif difB == 0:
						frase_expl2 = frase_expl2 + "a més, has aconseguit augmentar els teus moviments possibles sense afectar els del rival. "
					else:
						frase_expl2 = frase_expl2 + "a més, has aconseguit restringir els moviments del rival augmentant els teus. "
					
				else:
					if difW == 0:
						frase_expl2 = frase_expl2 + "però, has restringit els teus moviments possibles sense afectar els del rival. "
					elif difB == 0:
						frase_expl2 = frase_expl2 + "però, has augmentat els moviments del teu rival sense afectar els teus. "
					else:
						frase_expl2 = frase_expl2 + "però, has restringit els teus moviments possibles augmentant els del teu rival. "

			elif (difW < 0 and difB>0) or (difW <= 0 and difB>0) or (difW < 0 and difB >= 0):
				if fen1.split()[1] == "w":
					if difB == 0:
						frase_expl2 = frase_expl2 + "però, has restringit els teus moviments possibles sense afectar els del rival. "
					elif difW == 0:
						frase_expl2 = frase_expl2 + "però, has augmentat els moviments del teu rival sense afectar els teus. "
					else:
						frase_expl2 = frase_expl2 + "però, has restringit els teus moviments possibles augmentant els del teu rival. "
				else:
					if difB == 0:
						frase_expl2 = frase_expl2 + "a més, has aconseguit restringir els moviments del rival. "
					elif difW == 0:
						frase_expl2 = frase_expl2 + "a més, has aconseguit augmentar els teus moviments possibles sense afectar els del rival. "
					else:
						frase_expl2 = frase_expl2 + "a més, has aconseguit restringir els moviments del rival augmentant els teus. "
						
			elif difW == 0 and difB == 0:
					frase_expl2 = frase_expl2 + "aquest moviment no afecta a la llibertat de moviment de la resta de peces. "


			if control:
				frase_expl2 = frase_expl2 + "Ha empitjorat el control d'aquesta peça sobre el taulell, ara veu menys caselles"
				if MLPcol>=0.5:
					frase_expl2 = frase_expl2 + ", a més, està a una columna lliure."
				else:
					frase_expl2 = frase_expl2 + "."
			
			else:
				frase_expl2 = frase_expl2 + "Ha millorat el control d'aquesta peça sobre el taulell, ara veu les mateixes o més caselles que abans"
				if MLPcol>=0.5:
					frase_expl2 = frase_expl2 + ", però, està a una columna lliure."
				else:
					frase_expl2 = frase_expl2 + "."
				
			if not mate:
				eval = "Avaluació del moviment: " + eval
			else: eval = "Mat en: " + eval
			
			return frase_expl,frase_expl2, eval		
	
	def convertTuple(self,Tuples):
		fen1,fen2 = Tuples
		inputs = []
		# convertir la cadena de 448 bits en una lista de 64 elements de 7 bits
		binary = self.fenToBinaryAllInSquares(fen1)
		
		# Split the string into 64 groups of 7 digits
		groups = [binary[i:i+7] for i in range(0, len(binary), 7)]

		binary_numbers = [int(group, 2) for group in groups]

		arr = np.array(binary_numbers, dtype=int)

		#fer el mateix amb el segon fen
		binary = self.fenToBinaryAllInSquares(fen2)
		
		# Split the string into 64 groups of 7 digits
		groups = [binary[i:i+7] for i in range(0, len(binary), 7)]

		binary_numbers = [int(group, 2) for group in groups]

		arr1 = np.array(binary_numbers, dtype=int)

		arr = np.concatenate((arr, arr1))
		inputs.append(arr)

		inputs = np.array(inputs)
		
		return inputs
        
	def fenToBinaryAllInSquares(self,fen):
		sections = fen.split(' ')

		binary = ""
		allbinary = ""
		fil, col = 1, 1

		#seguent jugador
		turn = "0" if (sections[1] == "w") else "1"

		for symbol in sections[0]:
			binary=""
			if symbol == '/':
				fil += 1
				col = 1
				pass
			else:
				if symbol.isdigit():
					#si es un espai en blanc
					for val in range(int(symbol)):

						binary += turn+"000000"
						allbinary +=binary
						binary=""
						col += 1
						
				else:
					pieceColour = "0" if symbol.isupper() else "1" #0 si es majuscula = blanc o 1 si es minuscula = negre
					pieceTypeFromSymbol = {
						'k': "110",
						'p': "001",
						'n': "010",
						'b': "011",
						'r': "100",
						'q': "101"
					}
					pieceType = pieceTypeFromSymbol[symbol.lower()]
					if symbol.lower() == "p": #e peó
						#mirar si es al pas
						
						enPassant = sections[3] if len(sections) > 3 else "-"
						enPassantBinary = ""

						if enPassant == "-":
							enPassantBinary = "0"
							
						else:
							#convertir la lletra
							column = int(ord(enPassant[0])-96) #retorna el valor en ASCII de 97 si es a, restem per tenir rang de 0-7
							
							#convertir el número
							row = int(enPassant[1])
							val = -2 if turn == "0" else +2
							row += val

							if column==col and row == fil:
								enPassantBinary = "1"
							else:
								enPassantBinary = "0"

						allbinary += turn+pieceColour+"0"+enPassantBinary+pieceType

					elif symbol.lower() == "r": #es torre
						#mirar drets enroc
						
						#drets d'enrocar
						castlingRights = sections[2] if len(sections) > 2 else "KQkq"
						
						castling="0"
						
						if "K" in castlingRights and col==8 and fil == 8:
							castling = "1"

						if "Q" in castlingRights and col==1 and fil == 8:
							castling = "1"

						if "k" in castlingRights and col==8 and fil == 1:
							castling = "1"

						if "q" in castlingRights and col==1 and fil == 1:
							castling = "1"
						
						allbinary += turn+pieceColour+castling+"0"+pieceType

					elif symbol.lower() == "k": #es rei
						castlingRights = sections[2] if len(sections) > 2 else "KQkq"
						castling = "0"
						if symbol.isupper() and ("K" in castlingRights or "Q" in castlingRights):
							castling = "1"

						if symbol.islower() and ("k" in castlingRights or "q" in castlingRights):
							castling = "1"

						allbinary += turn+pieceColour+castling+"0"+pieceType

					
					else: #es qualsevol altra peça

						allbinary += turn+pieceColour+"0"+"0"+pieceType
					
					col += 1
				

		return allbinary

	def calexplanations(self,fen1,fen2):
		self.stockfish.set_fen_position(fen1)
		evaluation1 = self.stockfish.get_evaluation()
		evaluation1 = evaluation1['value']
		mate1 = 0
		mate2 = 0
		piece = self.get_piece(fen1, fen2)
		#evaluate FEN with stockfish and save pair
		self.stockfish.set_fen_position(fen2)
		evaluation2 = self.stockfish.get_evaluation()

		if evaluation2['type'] == 'cp':
			evaluation2 = evaluation2['value']

		else:
			mate2 = 1
			evaluation2 = evaluation2['value']   

		#If it is mate, the evaluation will be that of the mate

		if (mate1 == 1 and mate2 == 1):
			evaluation = int(evaluation2) - int(evaluation1)
			mate = 1
			textmate = "Dos son mate"

		elif (mate1 == 0 and mate2 == 0):
			evaluation = int(evaluation2) - int(evaluation1)
			mate = 0
			textmate = "normal"

		elif mate1 == 1 and mate2 == 0:
			evaluation = int(int(evaluation2) - round((1000/int(evaluation1)),0))
			mate = 0
			textmate = "Mate pos1"
			
		else:
			evaluation = int(round((1000/int(evaluation2)),0) - int(evaluation1))
			mate = 1
			textmate = "Mate pos2"

		return ([evaluation,piece,mate,textmate])

	def get_piece(self, fen1, fen2):
		PiecesTonNum = {
		"p": "1",
		"n": "2",
		"b": "3",
		"r": "4",
		"q": "5",
		"k": "6"
		}
		#check if there has been a capture
		a = b = 0
		codifsencera1 = codifsencera2 = ""
		for elem in fen1:
			if not elem.isdigit() and elem != "/":
				a += 1
				codifsencera1 += elem
			elif elem == "/":
				codifsencera1 += elem
			else:
				codifsencera1 += ("1" * int(elem))
			

		for elem in fen2:
			if not elem.isdigit() and elem != "/":
				b += 1
				codifsencera2 += elem
			elif elem == "/":
				codifsencera2 += elem
			else:
				codifsencera2 += ("1" * int(elem))
				
			
		col = 0
		fil = 0
		count = 0
		position1 = 0
		#checking which piece moved
		for elem in codifsencera2:

			if elem.isdigit() and elem != codifsencera1[count] and codifsencera1[count].isascii(): 
				piece = codifsencera1[count]
				return PiecesTonNum[piece.lower()]
				
			if elem == "/" and position1 == 0:
				fil += 1
				col = -1
		
			col += 1
			count += 1
		
		return PiecesTonNum[piece.lower()]

	def definirmoviment(self, fen1, fen2, moved):
		PiecesTonNum = {
		"p": "1",
		"n": "2",
		"b": "3",
		"r": "4",
		"q": "5",
		"k": "6"
		}

		center = [27, 28, 35, 36]
		outside = [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 31, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63]

		board1 = chess.Board(fen1)
		board2 = chess.Board(fen2)

		fen1 = fen1.split()
		fen2 = fen2.split()

		#check if there has been a capture
		a = b = 0
		codifsencera1 = codifsencera2 = ""
		for elem in fen1[0]:
			if not elem.isdigit() and elem != "/":
				a += 1
				codifsencera1 += elem
			elif elem == "/":
				codifsencera1 += elem
			else:
				codifsencera1 += ("1" * int(elem))
			

		for elem in fen2[0]:
			if not elem.isdigit() and elem != "/":
				b += 1
				codifsencera2 += elem
			elif elem == "/":
				codifsencera2 += elem
			else:
				codifsencera2 += ("1" * int(elem))
		

		col = 0
		fil = 0
		count = 0
		position1 = 0
		#checking which piece moved
		for elem in codifsencera2:

			if elem.isdigit() and elem != codifsencera1[count] and codifsencera1[count].isascii():
				if moved == PiecesTonNum[codifsencera1[count].lower()]:   
					piece = codifsencera1[count]
					position1 = (7-fil)*8 + col
				
			if elem == "/" and position1 == 0:
				fil += 1
				col = -1
		
			col += 1
			count += 1

		col = 0
		fil = 0
		count = 0
		position2 = 0
		#checking which piece moved
		for elem in codifsencera1:
			if elem.isdigit() and elem != codifsencera2[count] and codifsencera2[count].isascii():
				if moved == PiecesTonNum[codifsencera2[count].lower()]:   
					piece = codifsencera2[count]
					position2 = (7-fil)*8 + col
				
			if elem == "/" and position2 == 0:
				fil += 1
				col = -1

			col += 1
			count += 1

		centre = 0
		mig = 0
		fora = 0
		if position2 in center:
			centre = 1
		elif position2 in outside:
			fora = 1
		else:
			mig = 1


		control = 0
		if len(board2.attacks(position2)) - len(board1.attacks(position1)) < 0:
			#perd d'algunes caselles
			control = 1

		captura = a-b #És captura
		check = 1 if board1.is_check() else 0 #Està en jaque

		return captura, check, centre, mig, fora, control

	def eval(self, eval,mate, fen1, fen2, moved):
		output_bin = []
		eval = eval/100
		#calcculating evaluation ranges
		interv1pos = 1 if eval < 0.25 else 0
		interv2pos = 1 if (eval >= 0.25  and eval < 0.5) else 0
		interv3pos = 1 if (eval >= 0.5  and eval < 0.75) else 0
		interv4pos = 1 if (eval >= 0.75  and eval < 1) else 0
		interv5pos = 1 if (eval >= 1  and eval < 1.25) else 0
		interv6pos = 1 if (eval >= 1.25  and eval < 1.5) else 0
		interv7pos = 1 if (eval >= 1.5  and eval < 2.5) else 0
		interv8pos = 1 if (eval >= 2.5  and eval < 3.5) else 0
		interv9pos = 1 if (eval >= 3.5  and eval < 4.5) else 0
		interv10pos = 1 if (eval >= 4.5) else 0
		interv1neg = 1 if (eval > -0.25 and eval<0) else 0
		interv2neg = 1 if (eval <= -0.25  and eval > -0.5) else 0
		interv3neg = 1 if (eval <= -0.5  and eval > -0.75) else 0
		interv4neg = 1 if (eval <= -0.75  and eval > -1) else 0
		interv5neg = 1 if (eval <= -1  and eval > -1.25) else 0
		interv6neg = 1 if (eval <= -1.25  and eval > -1.5) else 0
		interv7neg = 1 if (eval <= -1.5  and eval > -2.5) else 0
		interv8neg = 1 if (eval <= -2.5  and eval > -3.5) else 0
		interv9neg = 1 if (eval <= -3.5  and eval > -4.5) else 0
		interv10neg = 1 if (eval <= -4.5) else 0

		output_bin.append(interv1pos)
		output_bin.append(interv2pos)
		output_bin.append(interv3pos)
		output_bin.append(interv4pos)
		output_bin.append(interv5pos)
		output_bin.append(interv6pos)
		output_bin.append(interv7pos)
		output_bin.append(interv8pos)
		output_bin.append(interv9pos)
		output_bin.append(interv10pos)
		output_bin.append(interv1neg)
		output_bin.append(interv2neg)
		output_bin.append(interv3neg)
		output_bin.append(interv4neg)
		output_bin.append(interv5neg)
		output_bin.append(interv6neg)
		output_bin.append(interv7neg)
		output_bin.append(interv8neg)
		output_bin.append(interv9neg)
		output_bin.append(interv10neg)

		#adding the mate bit
		output_bin.append(mate)

		captura, escac, centre, mig, exterior, control = self.definirmoviment(fen1, fen2, moved)
		output_bin.append(captura)
		output_bin.append(escac)
		output_bin.append(centre)
		output_bin.append(mig)
		output_bin.append(exterior)
		output_bin.append(control)

		#checking if piece attacks new ones
		arr1 = np.array(output_bin, dtype=float)

		return arr1
