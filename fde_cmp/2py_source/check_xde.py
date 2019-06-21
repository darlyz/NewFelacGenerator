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
color = {'Error': Fore.MAGENTA, 'Warn': Fore.CYAN, 'Empha': Fore.GREEN}

import re as regx
import os

error = False

def check_xde(ges_info, xde_lists, list_addr):

    # check disp
    if 'disp' in xde_lists:
        pass
    else:
        error_type  = not_declared('SHAP', 'Error')
        sgest_info  = "May be declared as 'DISP * *' in the first garaph, "
        sgest_info += "and '* *' could be referened in 'mdi' file.\n"
        report_error('*', error_type + sgest_info)

    # check coor
    if 'coor' in xde_lists: pass
        #xde_axi       =  ''.join(xde_lists['coor'])
        #xde_coor_strs = ' '.join(xde_lists['coor'])
        #if ext_name not in ['fde','cde','vde',pde'] and xde_axi != axi :
        #    addon_info    = "'{}' is not consistent with '{}' ".format(xde_coor_strs,axi)
        #    addon_info += "declared by mdi file.\n"
        #    error_form(line_num, '', addon_info)
    else:
        error_type  = not_declared('COOR', 'Error')
        sgest_info  = "May be declared as 'COOR {}' " \
                      .format(' '.join(list(ges_info['axi'])))
        sgest_info += "in the first garaph.\n"
        report_error('*', error_type + sgest_info)

    # check shap
    if 'shap' in xde_lists:
        check_shap(ges_info, xde_lists, list_addr)
    else:
        error_type  = not_declared('SHAP', 'Error')
        sgest_info  = "Shap function may be declared as "
        sgest_info += "'SHAP %1 %2' in the first garaph."
        report_error('*', error_type + sgest_info)

    # check gaus
    if 'gaus' in xde_lists:
        pass
    else:
        error_type  = not_declared('GAUS', 'Error')
        sgest_info  = "gauss integral may be declared as "
        sgest_info += "'GAUS %3' in the first garaph."
        report_error('*', error_type + sgest_info)

    # check insert code
    c_declares_BFmate = set()
    check_code(ges_info, xde_lists, list_addr, c_declares_BFmate)

    print('Error=',error)
    return error
# end check_xde()

def check_shap(ges_info, xde_lists, list_addr):

    # save all shap function name to shap_name_list
    pfelacpath = os.environ['pfelacpath']
    path_shap = pfelacpath + 'ges/gessub'
    file_shap = open(path_shap, mode='r')
    shap_name_list = [shap_name.rstrip() \
        for shap_name in file_shap.readlines() \
            if shap_name.split('.')[1] == 'sub\n']
    file_shap.close()

    base_shap_dclr_times = 0
    base_shap_line = 0

    for shap_list, line_num in zip(xde_lists['shap'], list_addr['shap']):

        if shap_list[0] == '%1':
            shap_form = ges_info['shap_form']
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
             shap_nodn = ges_info['shap_nodn']
        elif shap_list[1] == '%4':
            if shap_form in shap_forms:
                shap_nodn = node_dgree1[shap_forms.index(shap_form)]
        elif  shap_list[1] == '%2c':
              shap_nodn = shap_list[1].replace('%2',ges_info['shap_nodn'])
        else: shap_nodn = shap_list[1]

        if shap_form not in shap_forms:
            error_type  = faultly_declared('SHAP', 'Error')
            sgest_info  = "the first variable of shap declaration must to be "
            sgest_info += f"one of {shap_forms}, or '%1'.\n"
            report_error(line_num, error_type + sgest_info)

        else:
            # base shap declare
            if len(shap_list) == 2:

                base_shap_dclr_times += 1
                if base_shap_dclr_times > 1 :                  
                    warn_type   = duplicate_declared('base shap', 'Warn')
                    sgest_info  = f'It has been declared at {Empha_color}{base_shap_line}.\n'
                    report_warn(line_num,warn_type + sgest_info)

                base_shap_form = shap_form
                if shap_list[1] == '%2':
                      base_shap_node = ges_info['shap_nodn']
                else: base_shap_node = shap_list[1]

                if base_shap_dclr_times == 1:
                    base_shap_line = line_num

                if shap_form in shap_forms:
                    snodn = shap_node[shap_forms.index(shap_form)]
                    if base_shap_node not in snodn:
                        error_type  = faultly_declared('shap', 'Error')
                        sgest_info  = "the second variable of shap declaration"
                        sgest_info += f" is suggested to be one of {snodn}.\n"
                        report_error(line_num, error_type + sgest_info)

            # advance shap declare
            elif len(shap_list) >= 3:

                if shap_form != base_shap_form:
                    error_type  = faultly_declared('SHAP', 'Error')
                    sgest_info  = 'the first variable must be same to base shap '
                    sgest_info += f"declared at line {Empha_color}{base_shap_line}"
                    report_error(line_num, error_type + sgest_info)

                # sub shap declare using mix element
                if shap_list[1] == '%4' or shap_list[1].isnumeric():

                    vars_list = [var for var in shap_list[2:] if not var.isnumeric()]

                    if len(set(vars_list)) != len(vars_list):
                        report_warn(line_num, 'variable duplicated.\n')

                    for var_name in set(vars_list):
                        if 'coef' not in xde_lists:
                            if 'disp' in xde_lists and \
                            var_name not in xde_lists['disp'] :
                                warn_type   = not_declared(var_name, 'Warn')
                                sgest_info  = 'It must be declared in disp.\n'
                                report_warn(line_num, warn_type + sgest_info)

                        else:
                            if  'disp' in xde_lists \
                            and var_name not in xde_lists['disp'] \
                            and var_name not in xde_lists['coef'] :
                                warn_type   = not_declared(var_name, 'Warn')
                                sgest_info  = 'It must be declared in disp or coef.\n'
                                report_warn(line_num, warn_type + sgest_info)

                    # base shap is not degree 2 or not coordinate with shap_form
                    base_index = shap_forms.index(base_shap_form)
                    if base_shap_node != node_dgree2[base_index]:
                        error_type  = faultly_declared('SHAP', 'Error')
                        sgest_info  = 'The second variable of base shap must to be '
                        sgest_info += Empha_color + node_dgree2[base_index]
                        sgest_info += Error_color + '(second order), '
                        sgest_info += 'since using mix order element.\n'
                        report_error(base_shap_line, error_type + sgest_info)

                    # sub shap is not coordinate with base or not coordinate with shap_form
                    if shap_nodn != node_dgree1[base_index]:
                        error_type  = faultly_declared('SHAP', 'Error')
                        sgest_info  = 'The second variable of mixed shap must to be '
                        sgest_info += Empha_color + node_dgree1[base_index]
                        sgest_info += Error_color + '(first order), '
                        sgest_info += 'since using mix order element.\n'
                        report_error(line_num, error_type + sgest_info)

                # penalty disp var shap declare
                elif shap_list[1] == '%2c' \
                or  (shap_list[1][-1] == 'c' \
                and  shap_list[1][:-1].isnumeric) :

                    vars_list = [var if var.find('_') == -1 else var.split('_')[0] \
                        for var in shap_list[2:] \
                            if not var.isnumeric()]

                    if len(set(vars_list)) != len(vars_list):
                        report_warn(line_num, 'variable duplicated.\n')

                    for var_name in set(vars_list):
                        if 'coef' in xde_lists:
                            if var_name in xde_lists['coef'] :
                                report_warn(line_num, faultly_declared(var_name, 'Warn') \
                                    + "It must not be declared in 'coef'.\n")
                            elif 'disp' in xde_lists \
                            and var_name not in xde_lists['disp'] :
                                report_warn(line_num, faultly_declared(var_name, 'Warn') \
                                    + "It must be declared in 'disp'.\n")
                        elif 'disp' in xde_lists \
                        and var_name not in xde_lists['disp'] :
                            report_warn(line_num, faultly_declared(var_name, 'Warn') \
                                + "It must be declared in 'disp'.\n")

                    # base shap is not degree 1 or not coordinate with shap_form
                    base_index = shap_forms.index(base_shap_form)
                    if base_shap_node != node_dgree1[base_index]:
                        error_type  = faultly_declared('SHAP', 'Error')
                        sgest_info  = 'The second variable of base shap must to be '
                        sgest_info += Empha_color + node_dgree2[base_index]
                        sgest_info += Error_color + '(first order), '
                        sgest_info += 'since using penalty element.\n'
                        report_error(base_shap_line, error_type + sgest_info)

                    # sub shap is not coordinate with base or not coordinate with shap_form
                    if shap_nodn != node_dgree1[base_index]:
                        error_type  = faultly_declared('SHAP', 'Error')
                        sgest_info  = 'The second variable of penalty shap must to be '
                        sgest_info += Empha_color + node_dgree1[base_index]
                        sgest_info += Error_color + '(first order), '
                        sgest_info += 'since using penalty element.\n'
                        report_error(line_num, error_type + sgest_info)

        if not shap_list[1].isnumeric() \
        and shap_list[1][-1] in ['m','a','v','p','e']:
            if 'd' + ges_info['dim'] + shap_form + shap_nodn + '.sub' not in shap_name_list:
                report_error(line_num, faultly_declared('SHAP', 'Error') + \
                    shap_form + shap_nodn + ' is not a valid shap.')
# end check_shap()

def check_code(ges_info, xde_lists, list_addr, c_declares_BFmate):

    # the inner declaration
    all_declares  = {'tmax','dt','nstep','itnmax','time'}
    all_declares |= {'tolerance','dampalfa','dampbeta'}
    all_declares |= {'it','stop','itn','end'}
    all_declares |= {'imate','nmate','nelem','nvar','nnode'}
    all_declares |= {'ngaus','igaus','det','ndisp','nrefc','ncoor'}

    # gather C declares and check code
    c_declares = all_declares.copy()
    c_declares_BFmate = all_declares.copy()
    c_declares_array  = all_declares.copy()

    for strs in ["disp","coef","coor","func"]:
        if strs in xde_lists:
            c_declares |= set(xde_lists[strs])

    assist = {}
    for addr in xde_lists["code"].keys():

        assist['stitch'] = ''
        assist['addrss'] = addr
        for code_strs, line_num in zip(xde_lists["code"][addr], list_addr["code"][addr]):

            code_key = regx.match(r'\$C[C6VP]|@[LAWSR]|COMMON|ARRAY',code_strs,regx.I)
            if code_key == None: continue
            assist['ckey'] = code_key  = code_key.group()
            assist['lkey'] = lower_key = code_key.lower()

            if lower_key not in ['$cc','$c6'] :
                code_strs = code_strs.replace(code_key,'').lstrip()

            if lower_key in ['$cc','$c6','common'] :
                if gather_declare(code_strs, line_num, assist, c_declares, c_declares_BFmate):
                    continue

            elif lower_key == 'array':
                vara_list = regx.split(r'ARRAY',code_strs,regx.I)[-1].strip().split(',')
                for var in vara_list:
                    if var.find('['): var = var.split('[')[0].strip()
                    c_declares.add(var.lstrip('*'))
                    c_declares_array.add(var.lstrip('*'))
                    if addr == 'BFmate': c_declares_BFmate.add(var.lstrip('*'))

            elif lower_key == '$cv':
                check_tensor_assign(code_strs, line_num, xde_lists, c_declares_array)

            elif lower_key == '$cp':
                check_complex_assign(code_strs, line_num, xde_lists, list_addr, c_declares_array, c_declares)

            elif lower_key in ['@l','@w','@s']:
                code_list = code_strs.split()

                if lower_key == '@l':
                    if check_operator(code_list, line_num, xde_lists, list_addr):
                        continue

# end check_code()

def gather_declare(code_strs, line_num, assist_dict, c_declares, c_declares_BFmate):
    # check $cc code
    code_key   = assist_dict['ckey']
    lower_key  = assist_dict['lkey']
    stitchline = assist_dict['stitch']
    c_dclr_key = r"char|int|long|short|double|float"
    c_dclr_exp = r"[a-z].*="
    c_func_exp = r"\w+\(.*\)"
    
    #if    code_strs[-1] != ';' and code_strs[-1] != '{' \
    #and code_strs[-1] != '}' and code_strs[-1] != ',':
    #    if len(code_strs) >16:
    #            err_strs = "'"+code_strs[:8]+'...'+code_strs[-8:]+"'"
    #    else: err_strs = "'"+code_strs+"'"
    #    warn_form(line_num, err_strs, "need ';' at the tial.\n")

    code_strs = stitchline + code_strs.replace(code_key,'').lstrip()
    if code_strs[-1] != ';':
        assist_dict['stitch'] = code_strs.replace(code_key,'').lstrip()
        return True    # continue
    else: assist_dict['stitch'] = ''

    # find c declaration sentence and gather the variables
    if regx.search(c_dclr_key, code_strs, regx.I) != None:
        if regx.search(c_func_exp, code_strs, regx.I) != None:
            return True   # continue

        code_list = code_strs.split(';')
        code_list.pop()
        
        for sub_strs in code_list:

            if regx.search(c_dclr_key, sub_strs.lstrip(), regx.I) == None:
                return True   # continue

            if regx.match(r'static',sub_strs,regx.I) != None:
                sub_strs = regx.sub(r'static', '', sub_strs, 0, regx.I).lstrip()
            sub_strs = regx.sub(c_dclr_key, '', sub_strs).lstrip()

            for var in sub_strs.split(','):
                if var.find('=') != -1:
                    var = regx.sub(r'=.*', '', var)

                if var.find('['):
                    var = var.split('[')[0].strip()

                c_declares.add(var.lstrip('*'))
                if assist_dict['addrss'] == 'BFmate':
                    c_declares_BFmate.add(var.lstrip('*'))
    else: return True
    return False
# end check_common_code()

def check_tensor_assign(code_strs, line_num, xde_lists, c_declares_array):
    pattern = regx.compile(r'\^?[a-z][a-z0-9]*(?:_[a-z])+',regx.I)
    tnsr_list = pattern.findall(code_strs)
    if len(tnsr_list) == 0:
        report_warn(line_num,"there is no tensor, need not to use '$CV'.")

    else:
        for tnsr in set(tnsr_list):
            tnsr_name = tnsr.split('_')[0]
            if tnsr.count('_') == 1:
                if  tnsr_name not in xde_lists['vect'] \
                and tnsr_name not in c_declares_array:
                    report_error(line_num, not_declared(tnsr_name, 'Error') + \
                        "It must declared by 'VECT' or 'ARRAY'.")
            elif tnsr.count('_') == 2:
                if  tnsr_name not in xde_lists['matrix'] \
                and tnsr_name not in c_declares_array:
                     report_error(line_num, not_declared(tnsr_name, 'Error') + \
                        "It must declared by 'MATRIX' or 'ARRAY'.")
# end check_tensor_assign()

def check_complex_assign(code_strs, line_num, xde_lists, list_addr, c_declares_array, c_declares):
    pattern = regx.compile(r'\^?[a-z]\w*',regx.I)
    temp_list = pattern.findall(code_strs)
    tnsr_list, vara_list = [], []

    for var in temp_list:
        if var.find('_') != -1:
            tnsr_list.append(var)
        else: vara_list.append(var)

    if len(vara_list) != 0:
        for var in set(vara_list):
            if var+'r' not in c_declares:
                report_error(line_num, not_declared('real of '+var, 'Error') + '\n')
            if var+'i' not in c_declares:
                report_error(line_num, not_declared('imag of '+var, 'Error') + '\n')
                
    if len(tnsr_list) != 0:
        
        check_tensor_assign(code_strs, line_num, xde_lists, c_declares_array)
        
        for tnsr in set(tnsr_list):

            tnsr_name = tnsr.split('_')[0]
            if tnsr_name in list_addr['vect']:
                tnsr_line = list_addr['vect'][tnsr_name]
            else: continue

            if tnsr.count('_') == 1:

                if tnsr_name not in xde_lists['vect'] \
                or tnsr_name in c_declares_array:
                    report_error(line_num, not_declared(tnsr_name, 'Error') + \
                        "It must declared by 'VECT'.\n")

                else:
                    for var in xde_lists['vect'][tnsr_name]: 
                        
                        if var+'r' not in c_declares:
                            error_type = not_declared(f'real of {var} in vector {tnsr_name}(line {tnsr_line})', 'Error')
                            report_error(line_num, error_type + '\n')

                        if var+'i' not in c_declares:
                            error_type = not_declared(f'imag of {var} in vector {tnsr_name}(line {tnsr_line})', 'Error')
                            report_error(line_num, error_type + '\n')

            elif tnsr.count('_') == 2:
                if tnsr_name not in xde_lists['matrix'] \
                or tnsr_name in c_declares_array:
                    report_error(line_num, not_declared(tnsr_name, 'Error') + \
                        "It must declared by 'matrix'.\n")
                else:
                    if  xde_lists['matrix'][tnsr_name][0].isnumeric() \
                    and xde_lists['matrix'][tnsr_name][1].isnumeric() :
                        matrix_list = xde_lists['matrix'][tnsr_name][2:].copy()
                    else:
                        matrix_list = xde_lists['matrix'][tnsr_name].copy()

                    matrix_line_nums = list_addr['matrix'][tnsr_name][1:].copy()

                    for vars_list, matr_line_num in zip(matrix_list, matrix_line_nums):
                        var_regx = regx.compile(r'[a-z][a-z0-9]*',regx.I)
                        for var in set(var_regx.findall(vars_list)):
                            if var+'r' not in c_declares:
                                error_type = not_declared(f'real of {var} in matrix {tnsr_name}(line {matr_line_num})', 'Error')
                                report_error(line_num, error_type + '\n')
                            if var+'i' not in c_declares:
                                error_type = not_declared(f'imag of {var} in matrix {tnsr_name}(line {matr_line_num})', 'Error')
                                report_error(line_num, error_type + '\n')
# end check_complex_assign()

def check_operator(code_list, line_num, xde_lists, list_addr ):

    # save all operator name to oprt_name_list
    pfelacpath = os.environ['pfelacpath']
    path_oprt = pfelacpath +'ges/pdesub'
    file_oprt = open(path_oprt, mode='r')
    oprt_name_list = [oprt_name.rstrip() for oprt_name in file_oprt.readlines()]     
    file_oprt.close()

    # oprt_dict['grad']['xy'] = ['x','y','u']
    oprt_dict = {}
    path_oprt = pfelacpath + 'ges/pde.lib'
    file_oprt = open(path_oprt,mode='r')
    for strs in file_oprt.readlines():
        regx_oprt = regx.search(r'[a-z]+\.[xyzros123d]+\(.*\)', strs, regx.I)
        if regx_oprt != None:
            oprt_name,oprt_vars = regx_oprt.group().split('(')[:2]
            oprt_name,oprt_axis = oprt_name.split('.')[:2]

            oprt_vars = oprt_vars.split(')')[0]
            vars_list = oprt_vars.split(',')

            if oprt_name not in oprt_dict:
                oprt_dict[oprt_name] = {}
            if oprt_name in oprt_dict \
            and oprt_axis not in oprt_dict[oprt_name]:
                oprt_dict[oprt_name][oprt_axis] = {}

            oprt_dict[oprt_name][oprt_axis]['vars'] = vars_list.copy()
            oprt_dict[oprt_name][oprt_axis]['axis'] \
                = [ strs for strs in vars_list if strs in list('xyzros')]
            oprt_dict[oprt_name][oprt_axis]['disp'] \
                = [ strs for strs in vars_list if strs not in list('xyzros')]
    file_oprt.close()

    # first check length of '@l' code
    oprt_len = len(code_list)
    if oprt_len > 1:
        if code_list[1] != 'n':
            if oprt_len == 2:
                report_error(line_num, unsuitable_form('', 'Error') \
                    + 'not enough information for operator.\n')
                return True
    else:
        report_error(line_num, unsuitable_form('', 'Error') \
            + 'not enough information for operator.\n')
        return True

    # check the operator in 'pde.lib' if or not
    if code_list[0].find('.') == -1:
        report_error(line_num, unsuitable_form('', 'Error') \
            + "operator name form as 'name.axi', such as 'grad.xyz'.\n")
        return True

    elif code_list[0] not in oprt_name_list:
        sgest_info  = Empha_color + code_list[0]
        sgest_info += Error_color + " is not a default operator."
        report_error(line_num, unsuitable_form('', 'Error') + sgest_info)
        return True

    # split operator name, axis, variables
    oprt_name, oprt_deed = code_list[:2]
    oprt_name, oprt_axis = oprt_name.split('.')[:2]
    if oprt_deed != 'n': oprt_objt = code_list[2]
    
    # expand the vector in operator variables
    vars_list = []
    for strs in code_list[3:len(code_list)]:
        if   strs.find('_') == -1:
            vars_list.append(strs)
        elif strs.count('_') == 1:
            vector = strs.split('_')[0]
            if vector not in xde_lists['vect']:
                not_declare(line_num,vector,"It must be declared by 'VECT'.\n")
            else:
                vars_list += xde_lists['vect'][vector]
        else:
            error_form(line_num,'',"only vector or scalar can be operator's variable.\n")
            error = True

    # replenish default variables
    if len(vars_list) == 0 \
    and oprt_name not in ['singular','vol']:
        if oprt_deed == 'f':
            vars_list += list(oprt_axis) \
                + xde_lists['disp'][:len(oprt_dict[oprt_name][oprt_axis]['disp'])]
        elif 'coef' in xde_lists and oprt_deed in ['c','v','m']:
            vars_list += list(oprt_axis) \
                + xde_lists['coef'][:len(oprt_dict[oprt_name][oprt_axis]['disp'])]

    # split axis and normal variables
    oprt_axis_list = []
    for strs in vars_list:
        if strs in list('xyzros'):
            oprt_axis_list.append(strs)
        else: break

    oprt_disp_list = vars_list.copy()
    for strs in oprt_axis_list:
        oprt_disp_list.remove(strs)
    
    else:
        # compare provided axis counting with which in 'pde.lib'
        need_len = len(oprt_dict[oprt_name][oprt_axis]['axis'])
        provided = len(oprt_axis_list)
        if provided != need_len :
            error_form(line_num,'',"need {} axis but provided {}.\n".format(need_len, provided))
            error = True


    # warning that operator's axis be not in accordance with 'coor' declaration
    if oprt_axis != xde_axi:
        addon_info    = "coordinate of operator " + Empha_color + "'" + oprt_axis + "'"
        addon_info += Warnn_color + " is not consistance with 'coor' declaration "
        addon_info += Empha_color + "'" + xde_coor_strs + "'" + Warnn_color + ' in line '
        addon_info += Empha_color + str(list_addr['coor']) + ', '
        addon_info += Warnn_color + "and please make sure that it is necessary to do so.\n"
        warn_form(line_num, '', addon_info)

    # 'n' means no variable
    if   oprt_deed.lower() == 'n': 
        if len(code_list) > 2:
            warn_form(line_num, '', "useless information after 'n'")
    
    
    elif oprt_deed.lower() in ['c','v','m']: 

        # normal variables of operator must be declared in 'COEF'
        if 'coef' not in xde_lists:
            dif_set = set(oprt_disp_list)
        else:
            dif_set = set(oprt_disp_list).difference(set(xde_lists['coef']))
        if len(dif_set) != 0:
            error_form(line_num,'',"'{}' must be declared in 'COEF'.\n".format(' '.join(list(dif_set))))
        
        # 'c' means resault of operator assigned to scalar (c code declared)
        if oprt_deed.lower() == 'c':
            if oprt_objt not in c_declares:
                not_declare(line_num,oprt_objt,'it must be declared before line {}.\n'.format(line_num))
        
        # 'v' means resault of operator assigned to vector (vect declared)
        elif oprt_deed.lower() == 'v':
            if oprt_objt not in xde_lists['vect']:
                not_declare(line_num,oprt_objt,"it must be declared by 'VECT'.\n")
        
        # 'm' means resault of operator assigned to matrix (matrix declared)
        elif oprt_deed.lower() == 'm':
            if oprt_objt not in xde_lists['matrix']:
                not_declare(line_num,oprt_objt,"it must be declared by 'MATRIX'.\n")
    
    # 'f' means resault of operator assigned to fvect or fmatr
    elif oprt_deed.lower() == 'f':

        # normal variables of operator must be declared in 'DISP'
        if 'disp' not in xde_lists:
            dif_set = set(oprt_disp_list)
        else:
            dif_set = set(oprt_disp_list).difference(set(xde_lists['disp']))
        if len(dif_set) != 0:
            error_form(line_num,'',"'{}' must be declared in 'DISP'.\n".format(' '.join(list(dif_set))))

        if  oprt_objt not in xde_lists['fvect'] \
        and oprt_objt not in xde_lists['fmatr']:
            not_declare(line_num,oprt_objt,"it must be declared by 'FVECT' or 'FMATR'.\n")

    else:
        error_form(line_num,'', \
            "first variable of operator must be one of '[n, c, v, m, f]'.\n")
# end check_operator()

def report(repr_type):
    def _report(func):
        def __report(line_num, addon_info):
            
            global error
            if repr_type == 'Error':
                error = True

            output  = color[repr_type] + repr_type +': line number '
            output += Empha_color + str(line_num) + ', '
            output += color[repr_type] + func(line_num, addon_info)
            print(output)
        return __report
    return _report

@report('Error')
def report_error(line_num, addon_info):
    return addon_info

@report('Warn')
def report_warn(line_num, addon_info):
    return addon_info

def faultly_declared(key_word, report_type):
    return f"{Empha_color}'{key_word}' {color[report_type]}is faultly declared. "

def not_declared(key_word, report_type):
    return f"{Empha_color}'{key_word}' {color[report_type]}not be declared. "

def duplicate_declared(key_word, report_type):
    return f"{Empha_color}'{key_word}' {color[report_type]}is duplicatedly declared. "

def unsuitable_form(form_info, report_type):
    return f"{Empha_color}'{form_info}' {color[report_type]}is not a suitable form. "