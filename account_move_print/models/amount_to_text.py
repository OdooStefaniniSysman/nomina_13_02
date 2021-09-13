# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


from openerp import tools
from openerp.tools.translate import _
from openerp.exceptions import UserError, ValidationError
from lxml import etree


UNIDADES = (
    '',     
    'UN ',  
    'DOS ', 
    'TRES ',
    'CUATRO ',
    'CINCO ', 
    'SEIS ',  
    'SIETE ', 
    'OCHO ',  
    'NUEVE ', 
    'DIEZ ',  
    'ONCE ',  
    'DOCE ',  
    'TRECE ', 
    'CATORCE ',
    'QUINCE ', 
    'DIECISEIS ',
    'DIECISIETE ',
    'DIECIOCHO ', 
    'DIECINUEVE ',
    'VEINTE '     
)                 
DECENAS = (       
    'VENTI',      
    'TREINTA ',   
    'CUARENTA ',  
    'CINCUENTA ', 
    'SESENTA ',   
    'SETENTA ',   
    'OCHENTA ',   
    'NOVENTA ',   
    'CIEN '       
)
             
CENTENAS = (      
    'CIENTO ',    
    'DOSCIENTOS ',
    'TRESCIENTOS ',
    'CUATROCIENTOS ',
    'QUINIENTOS ',   
    'SEISCIENTOS ',  
    'SETECIENTOS ',  
    'OCHOCIENTOS ',  
    'NOVECIENTOS '   
)

def amount_to_text(self, number_in):
                              
    converted = ''                              

    if type(number_in) != 'str':
      number = str(number_in)   
    else:                       
      number = number_in        
                                                           
    number_str=number                                      
                                                           
    try:                                                   
      number_int, number_dec = number_str.split(".")       
    except ValueError:                                     
      number_int = number_str                              
      number_dec = ""                                      

    number_str = number_int.zfill(9)
    millones = number_str[:3]       
    miles = number_str[3:6]         
    cientos = number_str[6:]        

    if(millones):
        if(millones == '001'):
            converted += 'UN MILLON '
        elif(int(millones) > 0):     
            converted += '%sMILLONES ' % __convertNumber(millones)
                                                                  
    if(miles):                                                    
        if(miles == '001'):                                       
            converted += 'MIL '                                   
        elif(int(miles) > 0):                                     
            converted += '%sMIL ' % __convertNumber(miles)        
    if(cientos):                                                  
        if(cientos == '001'):                                     
            converted += 'UN '                                    
        elif(int(cientos) > 0):                                   
            converted += '%s ' % __convertNumber(cientos)        

    if number_dec == "":
      number_dec = "00" 
    if (len(number_dec) < 2 ):
      number_dec+='0'         
    
    #if (float(number_dec) > 0.001 ):
    #  converted += 'con '+ __convertDecimales(number_dec)

    return converted
                    
def __convertNumber(n):
    output = ''

    if(n == '100'):
        output = "CIEN "
    elif(n[0] != '0'):
        output = CENTENAS[int(n[0])-1]

    k = int(n[1:])
    if(k <= 20):
        output += UNIDADES[k]
    else:
        if((k > 30) & (n[2] != '0')):
            output += '%sY %s' % (DECENAS[int(n[1])-2], UNIDADES[int(n[2])])
        else:
            output += '%s%s' % (DECENAS[int(n[1])-2], UNIDADES[int(n[2])])

    return output
def __convertDecimales(n):
    output=""
    if n=='01':
     output='UN'
    if n=='02':
     output='DOS'
    if n=='03':
     output='TRES'
    if n=='04':
     output='CUATRO'
    if n=='05':
     output='CINCO'
    if n=='06':
     output='SEIS'
    if n=='07':
     output='SIETE'
    if n=='08':
     output='OCHO'
    if n=='09':
     output='NUEVE'
    if n=='10':
     output='DIEZ'
    if n=='11':
     output='ONCE'
    if n=='12':
     output='DOCE'
    if n=='13':
     output='TRECE'
    if n=='14':
     output='CATORCE'
    if n=='15':
     output='QUINCE'
    if n=='16':
     output='DIECISEIS'
    if n=='17':
     output='DIECISIETE'
    if n=='18':
     output='DIECIOCHO'
    if n=='19':
     output='DIECINUEVE'
    if n=='20':
     output='VEINTE'
    if n=='21':
     output='VEINTIUN'
    if n=='22':
     output='VEINTIDOS'
    if n=='23':
     output='VEINTITRES'
    if n=='24':
     output='VEINTICUATRO'
    if n=='25':
     output='VEINTICINCO'
    if n=='26':
     output='VEINTISEIS'
    if n=='27':
     output='VEINTISIETE'
    if n=='28':
     output='VEINTIOCHO'
    if n=='29':
     output='VEINTINUEVE'
    if n=='30':
     output='TREINTA'
    if n=='31':
     output='TREINTA Y UN'
    if n=='32':
     output='TREINTA Y DOS'
    if n=='33':
     output='TREINTA Y TRES'
    if n=='34':
     output='TREINTA Y CUATRO'
    if n=='35':
     output='TREINTA Y CINCO'
    if n=='36':
     output='TREINTA Y SEIS'
    if n=='37':
     output='TREINTA Y SIETE'
    if n=='38':
     output='TREINTA Y OCHO'
    if n=='39':
     output='TREINTA Y NUEVE'
    if n=='40':
     output='CUARENTA'
    if n=='41':
     output='CUARENTA Y UN'
    if n=='42':
     output='CUARENTA Y DOS'
    if n=='43':
     output='CUARENTA Y TRES'
    if n=='44':
     output='CUARENTA Y CUATRO'
    if n=='45':
     output='CUARENTA Y CINCO'
    if n=='46':
     output='CUARENTA Y SEIS'
    if n=='47':
     output='CUARENTA Y SIETE'
    if n=='48':
     output='CUARENTA Y OCHO'
    if n=='49':
     output='CUARENTA Y NUEVE'
    if n=='50':
     output='CINCUENTA'
     
    if n=='51':
     output='CINCUENTA Y UN'
    if n=='52':
     output='CINCUENTA Y DOS'
    if n=='53':
     output='CINCUENTA Y TRES'
    if n=='54':
     output='CINCUENTA Y CUATRO'
    if n=='55':
     output='CINCUENTA Y CINCO'
    if n=='56':
     output='CINCUENTA Y SEIS'
    if n=='57':
     output='CINCUENTA Y SIETE'
    if n=='58':
     output='CINCUENTA Y OCHO'
    if n=='59':
     output='CINCUENTA Y NUEVE'
    if n=='60':
     output='SESENTA'
    if n=='61':
     output='SESENTA Y UN'
    if n=='62':
     output='SESENTA Y DOS'
    if n=='63':
     output='SESENTA Y TRES'
    if n=='64':
     output='SESENTA Y CUATRO'
    if n=='65':
     output='SESENTA Y CINCO'
    if n=='66':
     output='SESENTA Y SEIS'
    if n=='67':
     output='SESENTA Y SIETE'
    if n=='68':
     output='SESENTA Y OCHO'
    if n=='69':
     output='SESENTA Y NUEVE'
    if n=='70':
     output='SETENTA'
    if n=='71':
     output='SETENTA Y UN'
    if n=='72':
     output='SETENTA Y DOS'
    if n=='73':
     output='SETENTA Y TRES'
    if n=='74':
     output='SETENTA Y CUATRO'
    if n=='75':
     output='SETENTA Y CINCO'
    if n=='76':
     output='SETENTA Y SEIS'
    if n=='77':
     output='SETENTA Y SIETE'
    if n=='78':
     output='SETENTA Y OCHO'
    if n=='79':
     output='SETENTA Y NUEVE'
    if n=='80':
     output='OCHENTA'
    if n=='81':
     output='OCHENTA Y UN'
    if n=='82':
     output='OCHENTA Y DOS'
    if n=='83':
     output='OCHENTA Y TRES'
    if n=='84':
     output='OCHENTA Y CUATRO'
    if n=='85':
     output='OCHENTA Y CINCO'
    if n=='86':
     output='OCHENTA Y SEIS'
    if n=='87':
     output='OCHENTA Y SIETE'
    if n=='88':
     output='OCHENTA Y OCHO'
    if n=='89':
     output='OCHENTA Y NUEVE'
    if n=='90':
     output='NOVENTA'
    if n=='91':
     output='NOVENTA Y UN'
    if n=='92':
     output='NOVENTA Y DOS'
    if n=='93':
     output='NOVENTA Y TRES'
    if n=='94':
     output='NOVENTA Y CUATRO'
    if n=='95':
     output='NOVENTA Y CINCO'
    if n=='96':
     output='NOVENTA Y SEIS'
    if n=='97':
     output='NOVENTA Y SIETE'
    if n=='98':
     output='NOVENTA Y OCHO'
    if n=='99':
     output='NOVENTA Y NUEVE'

    return output
