'''
 Copyright: Copyright (c) 2019
 Created: 2019-8-15
 Author: Zhang_Licheng
 Title: parse the sch file and check it
 All rights reserved
'''
from colorama import init, Fore, Back, Style
init(autoreset=True)
Error_color = Fore.MAGENTA
Warnn_color = Fore.CYAN
Empha_color = Fore.GREEN

import re
import json
from gensch import gen_obj, ifo_folder

dict_check = {'pre':1, 'sec':1, 'fnl':1}
addr_check = {'pre':1, 'sec':1, 'fnl':1}

def parse_sch(sch_dict, sch_addr, schfile):

    # parse xde to features and workflow features
    # just push the sentence into dict
    # report the meaningless sentence and paragraph declaration error
    pre_parse(sch_dict, sch_addr, schfile)

    # a simple parsing feature sentence to list
    # and check the duplicated of some feature declaration
    sec_parse(sch_dict, sch_addr)
    
    # fully check all features 
    #if gen_obj['check'] > 0:
    #    if check_xde(sch_dict, sch_addr):
    #        return True
 
    # parse features into a readable and transable style
    #fnl_parse(sch_dict, sch_addr)

    return False

def pre_parse(sch_dict, sch_addr, schfile):

    # all the sch keys
    key_pattern = r'DEFI|STIF|MASS|DAMP|LOAD|TYPE|MDTY|INIT|COEF|' \
                + r'EQUATION|SOLUTION|@SUBET|@head|@NBDE|END'

    keywd_tag = {'paragraph': 'DEFI'}

    line_i = 0
    stitchline = ''

    # parsing while read sch to sch_dict
    for line in schfile.readlines():
        line_i += 1

        # skip comment line and blank line
        if re.match(r'\s*(\$c[c6])?\s*((\\|//).*)?\s*\n',line,re.I) != None:
            continue

        # deal with valid sentence with comment
        # identify comment and stitch the next line begin with '\'
        line = stitchline + line
        if line.find('\\') != -1 :
            stitchline = line.split('\\')[0]
            continue
        else: stitchline = ''

        # identify comment begin with '//'
        if line.find('//') != -1:
            line = line.split('//')[0]

        # pop the space from head and tail
        line = line.strip()

        # retrieve the keywords
        matched_key = re.match(key_pattern, line, re.I)

        # find the keyword at the head
        if matched_key != None:

            key_match = matched_key.group()
            key_lower = key_match.lower()

            if key_lower in ['equation', '@subet', '@head', '@nbde']:

                keywd_tag['paragraph'] = key_lower

                if key_lower not in sch_dict:
                    sch_dict[key_lower] = []
                    sch_addr[key_lower] = []

                continue

            elif key_lower in ['stif', 'mass', 'damp', 'load', 'type', 'mdty', 'init']:

                if 'defi' not in sch_dict:
                    sch_dict['defi'] = {}
                    sch_addr['defi'] = {}

                sch_dict['defi'][key_lower] = line.replace(key_match,'').lstrip()
                sch_addr['defi'][key_lower] = line_i

            elif key_lower == 'coef':

                sch_dict['coef'] = line.replace(key_match,'').lstrip()
                sch_addr['coef'] = line_i

            elif key_lower == 'solution':

                keywd_tag['paragraph'] = 'solution'

                if 'solution' not in sch_dict:
                    sch_dict['solution'] = []
                    sch_addr['solution'] = []

                sch_dict['solution'].append( line.replace(key_match,'').lstrip() )
                sch_addr['solution'].append( line_i )


        # find the non-keyword-head line in 'EQUATION' 'SOLUTION' '@SUBET', '@head' and '@NBDE' paragraph
        else:
            para_key = keywd_tag['paragraph']

            sch_dict[para_key].append( line )
            sch_addr[para_key].append( line_i )

    export_parsing_result('pre', sch_dict, sch_addr)
# end pre_parse()

def sec_parse(sch_dict, sch_addr):

    # parse equation paragraph
    equa_list = sch_dict['equation'].copy()
    equa_addr = sch_addr['equation'].copy()

    sch_dict['equation'] = {}
    sch_addr['equation'] = {}

    equa_pattern = re.compile(r'VECT|READ|MATRIX|FORC',re.I)

    for equa_i, equa_str in enumerate(equa_list):

        matched_key = equa_pattern.match(equa_str).group()
        
        if matched_key != None:

            key_lower = matched_key.lower()

            equa_str  = equa_str.replace(matched_key,'').lstrip()

            if key_lower == 'vect':

                if 'vect' not in sch_dict['equation']:
                    sch_dict['equation']['vect'] = []
                    sch_addr['equation']['vect'] = []

                sch_dict['equation']['vect'].append(equa_str.split(','))
                sch_addr['equation']['vect'].append(equa_addr[equa_i])

            elif key_lower == 'read':

                if 'read' not in sch_dict['equation']:
                    sch_dict['equation']['read'] =[]
                    sch_addr['equation']['read'] =[]

                sch_dict['equation']['read'].append(equa_str)
                sch_addr['equation']['read'].append(equa_addr[equa_i])

            elif key_lower in ['matrix','forc']:

                if key_lower not in sch_dict['equation']:
                    sch_dict['equation'][key_lower] = []
                    sch_addr['equation'][key_lower] = []

                sch_dict['equation'][key_lower].append(equa_str.lstrip('=').lstrip())
                sch_addr['equation'][key_lower].append(equa_addr[equa_i])

    # parse solution paragraph
    equa_list = sch_dict['solution'].copy()
    equa_addr = sch_addr['solution'].copy()

    sch_dict['solution'] = {}
    sch_addr['solution'] = {}

    for equa_i, equa_str in enumerate(equa_list):

        if equa_i == 0:
            sch_dict['solution']['obj'] = equa_str
            sch_addr['solution']['obj'] = equa_addr[equa_i]

        else:
            if re.match(r'VECT',equa_str, re.I) != None:

                if 'vect' not in sch_dict['solution']:
                    sch_dict['solution']['vect'] = []
                    sch_addr['solution']['vect'] = []

                sch_dict['solution']['vect'].append(equa_str[4:].lstrip().split(','))
                sch_addr['solution']['vect'].append(equa_addr[equa_i])

            else:

                if 'code' not in sch_dict['solution']:
                    sch_dict['solution']['code'] = []
                    sch_addr['solution']['code'] = []

                sch_dict['solution']['code'].append(equa_str)
                sch_addr['solution']['code'].append(equa_addr[equa_i])

    export_parsing_result('sec', sch_dict, sch_addr)
# end sec_parse()


def export_parsing_result(stage, xde_dict, xde_addr):
    if dict_check[stage] != 0:
        file = open(ifo_folder + stage + '_check.json', mode='w')
        file.write(json.dumps(xde_dict,indent=4))
        file.close()
    if addr_check[stage] != 0:
        file = open(ifo_folder + stage + '_addr.json',  mode='w')
        file.write(json.dumps(xde_addr,indent=4))
        file.close()
# end export_parsing_result()