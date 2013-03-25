#patterns.py
import re

def getDictTrans():
	'''returns translation dictionary of malayalam 
	letter eg-{'kh':u'\u0b04',..}'''
	swarangal={
		'a':  u'\u0d05',
		'aa': u'\u0d06', 
		'A':  u'\u0d06',
		'i':  u'\u0d07',
		'ee':  u'\u0d08',
		'u':  u'\u0d09',
		'oo':  u'\u0d0a',
		'R~':  u'\u0d0b',
		'e':  u'\u0d0e',
		'E':  u'\u0d0f',
		'ai':  u'\u0d10',
		'o':  u'\u0d12',
		'O':  u'\u0d13',
		'au':  u'\u0d14',
		'am':  u'\u0d02',
		#'a:':'res'
	}

	venjanangal={
		'k': u'\u0d15', 
		'kh': u'\u0d16',
		'g': u'\u0d17',
		'gh': u'\u0d18',
		'ng': u'\u0d19','nng':u'\u0d19\u0d4d\u0d19',
		
		'ch': u'\u0d1a',
		'chh': u'\u0d1b',
		'j': u'\u0d1c',
		'jh': u'\u0d1d',
		'nj': u'\u0d1e',
		
		't': u'\u0d31\u0d4d\u0d31',
		'T': u'\u0d1f',
		'Th': u'\u0d20',
		
		'D': u'\u0d21',
		'Dh': u'\u0d22',
		'N': u'\u0d23','NN':u'\u0d23\u0d4d\u0d23',
		
		'th': u'\u0d24', 
		'thh': u'\u0d25',
		'd': u'\u0d26',
		'dh': u'\u0d27',
		'n': u'\u0d28','nn': u'\u0d28\u0d4d\u0d28',
		
		'p': u'\u0d2a',
		'ph': u'\u0d2b',
		'f': u'\u0d2b', 
		'b': u'\u0d2c',
		'bh': u'\u0d2d',
		'm': u'\u0d2e',
		
		'y': u'\u0d2f',
		'r': u'\u0d30', 
		'l': u'\u0d32', 'll': u'\u0d32\u0d4d\u0d32',
		'v': u'\u0d35',
		'S': u'\u0d36',
		'sh': u'\u0d37', 
		's': u'\u0d38', 
		'h': u'\u0d39',
		'L': u'\u0d33','LL': u'\u0d33\u0d4d\u0d33',
		'zh': u'\u0d34', 
		'R': u'\u0d31',
		
		
		'Nd':u'\u0d23\u0d4d\u0d1f'
	}

	chillukal={
		'aa': u'\u0d3e',
		'A':  u'\u0d3e',
		'e':  u'\u0d46',
		'ee':  u'\u0d40', 
		'R~':  u'\u0d43', 
		'am':  u'\u0d02', 
		'um ': u'\u0d41\u0d02 ',
		'o':  u'\u0d4a',
		'i':  u'\u0d3f', 
		'ai':  u'\u0d48', 
		'u':  u'\u0d41', 
		'a':  '',
		'O':  u'\u0d4b', 
		'E':  u'\u0d47', 
		'au':  u'\u0d57', 
		'oo':  u'\u0d42',
		'virama':u'\u0d4d'
		}
		
	# we do not add anything(swarangal) with these letters	
	n_r_l = {
		'N':u'\u0d23\u0d4d\u200d',
		'n':u'\u0d28\u0d4d\u200d',
		'r':u'\u0d30\u0d4d\u200d',
		'l':u'\u0d32\u0d4d\u200d',
		'L':u'\u0d33\u0d4d\u200d',
		
		'nte':u'\u0d28\u0d4d\u0d31\u0d46',
		'ntE':u'\u0d28\u0d4d\u0d31\u0d47',
		}
		
	dict_letters=combine_dicts(swarangal,n_r_l)  #A,aa,i,I
	for venj in venjanangal.keys(): #k,kh,g,gh..
		for chil in chillukal.keys():   #A,aa,i..
			venj_chil=venj+chil    #kA,kaa....
			if chil=='virama':      #not want to add 'kvirama,Kvirama etc
				venj_chil=venj #not add anything k,kh,g,gh...
				if venj in 'NnrlL':
					venj_chil=venj+'~'
					dict_letters[venj*2]=(venjanangal[venj]+chillukal[chil])*2
			
			dict_letters[venj_chil]=venjanangal[venj]+chillukal[chil]
	return dict_letters
	
def combine_dicts(d1,d2):
	for k,v in d2.iteritems():
		d1[k]=v
	return d1
	
def getPat():
	p1='(kh?|gh?|nn?g|NN|nn|ll|LL|ch?h?|jh?|nj|th?h?|Th?|dh?|Dh?|Nd?|n|ph?|f|bh?|y|r|l|v|S|sh|s|h|L|zh|R|m?)'
	p2='(aa|A|i|ee|um\s|u|oo|R~|e|E|ai|I|o|O|au|am|a?)'
	
	pat='^'+p1+p2
	return pat
	
def transword(wd):
	dict_trans=getDictTrans()
	pattern=getPat()
	trans=''
	while len(wd)>0:
		M=re.match('^(R~|N~|n~|r~|l~|L~|nte|ntE)',wd)
		if not M: M=re.match(pattern,wd)
		
		if M.group(0) in dict_trans.keys():
			trans+=dict_trans[M.group(0)]
			wd=wd[M.end():]
		else:
			trans+=wd[0]
			wd=wd[1:]
	return trans
