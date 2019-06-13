'''
 Copyright: Copyright (c) 2019
 Created: 2019-4-28
 Author: Zhang_Licheng
 Title: check the xde file
 All rights reserved
'''
from colorama import init, Fore, Back, Style
init(autoreset=True)
Error_color = Fore.MAGENTA
Warnn_color = Fore.CYAN
Empha_color = Fore.GREEN

color={'Error':Fore.MAGENTA,'Warnn':Fore.CYAN,'Empha':Fore.GREEN}

import re as regx
import os


def check_xde(xde_lists, list_addr, ges_shap_type, ges_gaus_type, coor_type):

  error = False

  #ges_shap_type = regx.search(r'[ltqwc][1-9]+',gesname,regx.I).group()
  #ges_gaus_type = regx.search(r'g[1-9]+',gesname,regx.I)
  #if ges_gaus_type != None:
  #  ges_gaus_type = ges_gaus_type.group()

  dim = regx.search(r'[1-9]+', coor_type, regx.I).group()
  axi = coor_type.split('d')[1]

  ges_shap_nodn = regx.search(r'[1-9]+', ges_shap_type, regx.I).group()
  ges_shap_form = ges_shap_type[0]

  coor_list = list(axi)
  coor_strs = ' '.join(coor_list)

  pfelacpath = os.environ['pfelacpath']
  path_shap = pfelacpath + 'ges/gessub'
  file_shap = open(path_shap, mode='r')
  shap_name_list = [shap_name.rstrip() \
    for shap_name in file_shap.readlines() \
      if shap_name.split('.')[1] == 'sub\n']
  file_shap.close()

  path_oprt = pfelacpath +'ges/pdesub'
  file_oprt = open(path_oprt, mode='r')
  oprt_name_list = [oprt_name.rstrip() \
    for oprt_name in file_oprt.readlines()]   
  file_oprt.close()

    # check disp
  if 'disp' in xde_lists:
    pass
  else:
    addon_info  = "may be declared as 'DISP * *' in the first garaph, "
    addon_info += "and '* *' could be referened in 'mdi' file.\n"
    not_declare('*','DISP',addon_info)
    error = True

  # check coor
  if 'coor' in xde_lists:
    xde_axi     =  ''.join(xde_lists['coor'])
    xde_coor_strs = ' '.join(xde_lists['coor'])
    # if ext_name not in ['fde','cde','vde',pde'] and xde_axi != axi :
    #   addon_info  = "'{}' is not consistent with '{}' ".format(xde_coor_strs,axi)
    #   addon_info += "declared by mdi file.\n"
    #   error_form(line_num, '', addon_info)
  else:
    addon_info  = "may be declared as 'COOR {}' ".format(coor_strs)
    addon_info += "in the first garaph.\n"
    not_declare('*','coor var',addon_info)
    error = True

  # check shap
  base_shap_dclr_times = 0
  base_shap_line = 0
  if 'shap' in xde_lists:

    for shap_list, line_num in zip(xde_lists['shap'], list_addr['shap']):

      if shap_list[0] == '%1':
          shap_form = ges_shap_form
      else: shap_form = shap_list[0]

      shap_node = [['%2','2','3'], \
                   ['%2','3','6'], \
                   ['%2','4','8','9'], \
                   ['%2','4','6','10','18'], \
                   ['%2','8','20','27'] ]
      shap_forms    = ['l','t','q','w','c']
      node_dgree1   = ['2','3','4','4','8']
      node_dgree1_5 = ['' ,'' ,'8','' ,'20']
      node_dgree2   = ['3','6','9','10','27']

      if   shap_list[1] == '%2':
           shap_nodn = ges_shap_nodn
      elif shap_list[1] == '%4':
        for sform, snodn in zip(shap_forms, node_dgree1):
          if shap_form == sform:
             shap_nodn = snodn
      elif  shap_list[1] == '%2c':
            shap_nodn = shap_list[1].replace('%2',ges_shap_nodn)
      else: shap_nodn = shap_list[1]

      if shap_form not in shap_forms:
        addon_info  = "the first variable of shap declaration must to be "
        addon_info += "one of {}, or '%1'.\n".format(shap_forms)
        fault_declare(line_num,'shap', addon_info)

      else:
        # base shap declare
        if len(shap_list) == 2:

          base_shap_dclr_times += 1
          if base_shap_dclr_times > 1 :
            duplicate_declare(line_num,'base shap','It has been declared at ' \
              +Empha_color + str(base_shap_line) +'.\n')

          base_shap_form = shap_form
          if shap_list[1] == '%2':
                base_shap_node = ges_shap_nodn
          else: base_shap_node = shap_list[1]

          if base_shap_dclr_times == 1:
             base_shap_line = line_num

          for sform, snodn in zip(shap_forms, shap_node):
            if shap_form == sform:
               if base_shap_node not in snodn:
                 fault_declare(line_num,'shap', \
                   'the second variable of shap declaration' + \
                     ' is suggested to be one of {}.\n'.format(snodn))

        # advance shap declare
        elif len(shap_list) >= 3:

          if shap_form != base_shap_form:
            fault_declare(line_num,'shap', \
              'the first variable must be same to base shap declared at line' \
                + Empha_color +' {}.\n'.format(base_shap_line))

          # sub shap declare using mix element
          if shap_list[1] == '%4' or shap_list[1].isnumeric():

            temp_list = shap_list[2:len(shap_list)]
            var_list  = [var for var in temp_list if not var.isnumeric()]

            if len(set(var_list)) != len(var_list):
              warn_form(line_num, '', 'variable duplicated.\n')

            for var_name in set(var_list):
              if 'coef' not in xde_lists:
                if var_name not in xde_lists['disp'] :
                  wnot_declare(line_num, var_name, \
                    'It must be declared in disp.\n')
              else:
                if  var_name not in xde_lists['disp'] \
                and var_name not in xde_lists['coef'] :
                  wnot_declare(line_num, var_name, \
                    'It must be declared in disp or coef.\n')

            if shap_list[1] == '%4':
              for sform, snodn in zip(shap_forms, node_dgree1):
                if shap_form == sform:
                  shap_nodn = snodn
            else: shap_nodn = shap_list[1]

            for sform, bnodn, snodn in zip(shap_forms, node_dgree2, node_dgree1):
              if base_shap_form == sform :

                # base shap is not degree 2 or not coordinate with shap_form
                if base_shap_node != bnodn :
                  addon_info = 'The second variable of base shap must to be '
                  addon_info += Empha_color + bnodn
                  addon_info += Error_color + '(second order), '
                  addon_info += 'since using mix order element.\n'
                  fault_declare(base_shap_line,'shap', addon_info)

                # sub shap is not coordinate with base or not coordinate with shap_form
                if shap_nodn != snodn:
                  addon_info  = 'The second variable of mixed shap must to be '
                  addon_info += Empha_color + snodn
                  addon_info += Error_color + '(first order), '
                  addon_info += 'since using mix order element.\n'
                  fault_declare(line_num,'shap', addon_info)

          # penalty disp var shap declare
          elif shap_list[1] == '%2c' \
          or  (shap_list[1][-1] == 'c' \
          and  shap_list[1][:-1].isnumeric) :

            temp_list = shap_list[2:len(shap_list)]

            var_list  = [var if var.find('_') == -1 else var.split('_')[0] \
              for var in temp_list \
                if not var.isnumeric()]

            if len(set(var_list)) != len(var_list):
              warn_form(line_num, '', 'variable duplicated.\n')

            for var_name in set(var_list):
              if 'coef' in xde_lists:
                if var_name in xde_lists['coef'] :
                  wrong_declare(line_num, var_name, \
                    'It must not be declared in coef.\n')
                elif var_name not in xde_lists['disp'] :
                  wnot_declare(line_num, var_name, \
                    'It must be declared in disp.\n')
              elif var_name not in xde_lists['disp'] :
                  wnot_declare(line_num, var_name, \
                    'It must be declared in disp.\n')

            for sform, bnodn, snodn in zip(shap_forms, node_dgree1, node_dgree1):
              if base_shap_form == sform :

                # base shap is not degree 1 or not coordinate with shap_form
                if base_shap_node != bnodn :
                  addon_info = 'The second variable of base shap must to be '
                  addon_info += Empha_color + bnodn
                  addon_info += Error_color + '(first order), '
                  addon_info += 'since using penalty element.\n'
                  fault_declare(base_shap_line,'shap', addon_info)

                # sub shap is not coordinate with base or not coordinate with shap_form
                if shap_nodn != snodn:
                  addon_info  = 'The second variable of mixed shap must to be '
                  addon_info += Empha_color + snodn
                  addon_info += Error_color + '(first order), '
                  addon_info += 'since using penalty element.\n'
                  fault_declare(line_num,'shap', addon_info)

        if not shap_list[1].isnumeric \
        and shap_list[-1] in ['m','a','v','p','e']:
          if 'd' + dim + shap_form + shap_nodn + '.sub' not in shap_name_list:
            fault_declare(line_num, 'shap', \
              shap_form + shap_nodn + 'is not a valid shap.')

  else:
    not_declare('*','shap function', \
      'may be declared as \'SHAP %1 %2\' in the first garaph.')
    error = True

  # check gaus
  if 'gaus' in xde_lists:
    pass
  else:
    not_declare('*','gauss integral', \
      'may be declared as \'GAUS %3\' in the first garaph.')
    error = True

  # the inner declaration
  all_declares  = {'tmax','dt','nstep','itnmax','time'}
  all_declares |= {'tolerance','dampalfa','dampbeta'}
  all_declares |= {'it','stop','itn','end'}
  all_declares |= {'imate','nmate','nelem','nvar','nnode'}
  all_declares |= {'ngaus','igaus','det','ndisp','nrefc','ncoor'}

  # gather C declares and check code
  c_declares = all_declares.copy()
  c_declares_BFmate = all_declares.copy()
  c_declares_array = all_declares.copy()
  for strs in ["disp","coef","coor","func"]:
    if strs in xde_lists:
      c_declares |= set(xde_lists[strs])

  c_dclr_key = r"char|int|long|short|double|float"
  c_dclr_exp = r"[a-z].*="
  c_func_exp = r"\w+\(.*\)"
  for addr in xde_lists["code"].keys():
    
    stitchline = ''

    for code_strs, line_num in zip(xde_lists["code"][addr], list_addr["code"][addr]):

      regx_key  = regx.match(r'\$C[C6VP]|@[LAWSR]|COMMON|ARRAY',code_strs,regx.I)
      if regx_key == None: continue
      regx_key  = regx_key.group()
      lower_key = regx_key.lower()

      if lower_key not in ['$cc','$c6'] :
        code_strs = code_strs.replace(regx_key,'').lstrip()
      
      if lower_key in ['$cc','$c6','common'] :

        # check $cc code
        if lower_key in ['$cc','$c6'] :
          if code_strs[3] != ' ':
            if len(code_strs) >16:
                err_strs = "'" + code_strs[:16] + '...' + "'"
            else: err_strs = "'" + code_strs + "'"
            error_form(line_num, err_strs, \
              "need space after '{}'.\n".format(regx_key))
        
          #if  code_strs[-1] != ';' and code_strs[-1] != '{' \
          #and code_strs[-1] != '}' and code_strs[-1] != ',':
          #  if len(code_strs) >16:
          #      err_strs = "'"+code_strs[:8]+'...'+code_strs[-8:]+"'"
          #  else: err_strs = "'"+code_strs+"'"
          #  warn_form(line_num, err_strs, "need ';' at the tial.\n")

        code_strs = stitchline + code_strs.replace(regx_key,'').lstrip()
        if code_strs[-1] != ';':
          stitchline = code_strs.replace(regx_key,'').lstrip()
          continue
        else: stitchline = ''

        # find c declaration sentence and gather the variables
        if regx.search(c_dclr_key, code_strs, regx.I) != None:
          if regx.search(c_func_exp, code_strs, regx.I) != None:
            continue

          code_list = code_strs.split(';')
          code_list.pop()
          
          for sub_strs in code_list:
            if regx.search(c_dclr_key, sub_strs.lstrip(), regx.I) == None:
              continue

            if regx.match(r'static',sub_strs,regx.I) != None:
              sub_strs = regx.sub(r'static', '', sub_strs, 0, regx.I).lstrip()
            sub_strs = regx.sub(c_dclr_key, '', sub_strs).lstrip()

            for var in sub_strs.split(','):
              if var.find('=') != -1:
                var = regx.sub(r'=.*', '', var)

              if var.find('['):
                var = var.split('[')[0].strip()

              c_declares.add(var.lstrip('*'))
              if addr == 'BFmate':
                c_declares_BFmate.add(var.lstrip('*'))
        else: continue

      elif lower_key == 'array':
        vara_list = regx.split(r'ARRAY',code_strs,regx.I)[-1].strip().split(',')
        for var in vara_list:
          if var.find('['):
            var = var.split('[')[0].strip()
          c_declares.add(var.lstrip('*'))
          c_declares_array.add(var.lstrip('*'))
          if addr == 'BFmate':
            c_declares_BFmate.add(var.lstrip('*'))

      elif lower_key == '$cv':
        pattern = regx.compile(r'\^?[a-z][a-z0-9]*(?:_[a-z])+',regx.I)
        tnsr_list = pattern.findall(code_strs)
        if len(tnsr_list) == 0:
          warn_form(line_num,'',"there is no tensor, need not to use '$CV'.")

        else:
          for tnsr in set(tnsr_list):
            tnsr_name = tnsr.split('_')[0]
            if tnsr.count('_') == 1:
              if  tnsr_name not in xde_lists['vect'] \
              and tnsr_name not in c_declares_array:
                not_declare(line_num, tnsr_name, \
                  "It must declared by 'VECT' or 'ARRAY'.")
                error = True
            elif tnsr.count('_') == 2:
              if  tnsr_name not in xde_lists['matrix'] \
              and tnsr_name not in c_declares_array:
                not_declare(line_num, tnsr_name, \
                  "It must declared by 'MATRIX' or 'ARRAY'.")
                error = True

      elif lower_key == '$cp':

        pattern = regx.compile(r'\^?[a-z]\w*',regx.I)
        temp_list = pattern.findall(code_strs)
        tnsr_list = []
        vara_list = []
        for var in temp_list:
          if var.find('_') != -1:
              tnsr_list.append(var)
          else: vara_list.append(var)

        if len(vara_list) != 0:
          for var in set(vara_list):
            if var+'r' not in c_declares:
              not_declare(line_num, 'real of ' +var,'\n')
              error = True
            if var+'i' not in c_declares:
              not_declare(line_num, 'imag of ' +var,'\n')
              error = True
        
        if len(tnsr_list) != 0:
          for tnsr in set(tnsr_list):
            tnsr_name = tnsr.split('_')[0]
            if tnsr.count('_') == 1:
              if tnsr_name not in xde_lists['vect'] \
              or tnsr_name in c_declares_array:
                not_declare(line_num, tnsr_name, \
                  "It must declared by 'VECT'.\n")
                error = True
              else:
                for var in xde_lists['vect'][tnsr_name]: 
                  if var+'r' not in c_declares:
                    not_declare(line_num, 'real of ' + var + ' in ' \
                      + tnsr_name + '(line {})' \
                        .format(list_addr['vect'][tnsr_name]),'\n')
                    error = True
                  if var+'i' not in c_declares:
                    not_declare(line_num, 'imag of ' + var + ' in ' \
                      + tnsr_name + '(line {})' \
                        .format(list_addr['vect'][tnsr_name]),'\n')
                    error = True
            elif tnsr.count('_') == 2:
              if tnsr_name not in xde_lists['matrix'] \
              or tnsr_name in c_declares_array:
                not_declare(line_num, tnsr_name, \
                  "It must declared by 'matrix'.\n")
                error = True
              else:
                if  xde_lists['matrix'][tnsr_name][0].isnumeric() \
                and xde_lists['matrix'][tnsr_name][1].isnumeric() :
                  matrix_list = xde_lists['matrix'][tnsr_name].copy()
                  matrix_list.pop(0)
                  matrix_list.pop(0)
                else:
                  matrix_list = xde_lists['matrix'][tnsr_name].copy()

                matrix_line_nums = list_addr['matrix'][tnsr_name].copy()
                matrix_line_nums.pop(0)

                for var_list, matr_line_num in zip(matrix_list, matrix_line_nums):
                  var_regx = regx.compile(r'[a-z][a-z0-9]*',regx.I)
                  for var in set(var_regx.findall(var_list)):
                    if var+'r' not in c_declares:
                      not_declare(line_num, 'real of ' + var + ' in matrix ' \
                        + tnsr_name + '(line {})' \
                          .format(matr_line_num),'\n')
                      error = True
                    if var+'i' not in c_declares:
                      not_declare(line_num, 'imag of ' + var + ' in matrix ' \
                        + tnsr_name + '(line {})' \
                          .format(matr_line_num),'\n')
                      error = True
      
      elif lower_key in ['@l','@w','@s'] :

        code_list = code_strs.split()
        print(lower_key, code_list)

        if lower_key == '@l':
          oprt_name = code_list[0]
          oprt_deed = code_list[1]

          if oprt_name not in oprt_name_list:
            addon_info  = Empha_color + oprt_name
            addon_info += Error_color + " is not a default operator."
            error_form(line_num, '', addon_info)

          oprt_axi = oprt_name.split('.')[1]
          if oprt_axi != xde_axi:
            addon_info  = "coordinate of operator " + Empha_color + "'" + oprt_axi + "'"
            addon_info += Warnn_color + " is not consistance with 'coor' declaration "
            addon_info += Empha_color + "'" + xde_coor_strs + "'" + Warnn_color + ' in line '
            addon_info += Empha_color + str(list_addr['coor']) + ', '
            addon_info += Warnn_color + "and please make sure that it is necessary to do so.\n"
            warn_form(line_num, '', addon_info)

          if   oprt_deed.lower() == 'n': 
            if len(code_list) > 2:
              warn_form(line_num, '', "useless information after 'n'")
          elif oprt_deed.lower() == 'c': pass
          elif oprt_deed.lower() == 'v': pass
          elif oprt_deed.lower() == 'm': pass
          elif oprt_deed.lower() == 'f': pass

          else:
            error_form(line_num,'', \
              "first variable of operator must be one of '[n, c, v, m, f]'.\n")
        

      elif lower_key in ['@a','@r'] :
        pass

  # check mate
  is_var = r'[a-z]\w*'
  for var in xde_lists['mate']:
    if regx.match(is_var, var, regx.I) != None :
      if var.find('['):
        var = var.split('[')[0]
      if var not in c_declares_BFmate:
        not_declare(list_addr['mate'], var, '\n')

  # check vect
  if 'vect' in xde_lists:
    for vect in xde_lists['vect'].keys():
      for strs in xde_lists['vect'][vect]:
        for var in regx.findall(r'[a-z]\w*', strs, regx.I):
          if var not in c_declares:
            not_declare(list_addr['vect'][vect], var, '\n')

  # check matrix
  if 'matrix' in xde_lists:
    for matrix in xde_lists['matrix'].keys():
      line_nums = list_addr['matrix'][matrix].copy()
      matr_name_line = line_nums.pop(0)

      matr_list = [var \
        for var in xde_lists['matrix'][matrix] \
          if not var.isnumeric()]

      row_lenth = set()
      for row,line_num in zip(matr_list,line_nums):
        row_list = row.split()
        row_lenth.add(len(row_list))
        for strs in row_list:
          for var in regx.findall(r'[a-z]\w*',strs,regx.I):
            if var not in c_declares:
              not_declare(line_num, var, '\n')

      if xde_lists['matrix'][matrix][0].isnumeric:
        row = xde_lists['matrix'][matrix][0]
        if xde_lists['matrix'][matrix][1].isnumeric:
          clm = xde_lists['matrix'][matrix][1]

          if len(matr_list) != int(row):
            fault_declare(matr_name_line, matrix, \
              'The matrix row is not in accordance with which defined.\n')
          if int(clm) not in row_lenth:
              fault_declare(matr_name_line, matrix, \
                'The matrix column is not in accordance with which defined.\n')
        else:
          fault_declare(matr_name_line, matrix, \
            'need to define row and column number at the same time.\n')

      if len(row_lenth) != 1:
        fault_declare(matr_name_line, matrix, \
          'lenth of every row is not equal.\n')

  # check fvect
  if 'fvect' in xde_lists:
    for name,lists in xde_lists['fvect'].items():
      if len(lists) != 1:
        fault_declare(list_addr['fvect'][name], name, \
          'sugest declare as \'FVECT {} [len]\'.\n'.format(name))
        error = True

  # check fvect
  if 'fmatr' in xde_lists:
    for name,lists in xde_lists['fmatr'].items():
      if len(lists) != 2:
        fault_declare(list_addr['fmatr'][name], name, \
          'sugest declare as \'FMATR {} [row] [clm]\'.\n'.format(name))
        error = True



  return error






def error(func):
  def _error(*args, **argv):
    output_words =  Error_color + 'error: line number '
    output_words += Empha_color + str(args[0]) +', '
    output_words += Error_color + func(*args, **argv)
    print(output_words)
  return _error

@error
def not_declare(line_num, declare_name, addon_info):
  return Empha_color + declare_name \
     + Error_color + " not be declared. {}".format(addon_info)

@error
def fault_declare(line_num, declare_name, addon_info):
  return Empha_color + declare_name \
     + Error_color + " faultly declared. {}".format(addon_info)

@error
def error_form(line_num, form_info, addon_info):
  return Empha_color + form_info \
     + Error_color + " error form, {}".format(addon_info)


def warn(func):
  def _warn(*args, **argv):
    output_words =  Warnn_color + 'warn: line number '
    output_words += Empha_color + str(args[0]) + ', '
    output_words += Warnn_color + func(*args, **argv)
    print(output_words)
  return _warn

@warn
def duplicate_declare(line_num, declare_name, addon_info):
  return Empha_color + declare_name \
     + Warnn_color + " is duplicately declared. {}".format(addon_info)

@warn
def wnot_declare(line_num, declare_name, addon_info):
  return Empha_color + declare_name \
     + Warnn_color + " not be declared. {}".format(addon_info)

@warn
def wrong_declare(line_num, declare_name, addon_info):
  return Empha_color + declare_name \
     + Warnn_color + " wrong declared. {}".format(addon_info)

@warn
def warn_form(line_num, form_info, addon_info):
  return Empha_color + form_info \
     + Warnn_color + " not suitable form, {}".format(addon_info)