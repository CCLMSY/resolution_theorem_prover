"""数据读取模块

读取输入文件，生成子句集合。

Functions:
    read_clauses() -> list[Clause]: 读取输入
"""

from data_structure import Func, Clause

# 读入和处理数据
cnt_var = 0 # 变量计数
cnt_const = 0 # 常量计数
const_map = dict() # 常量映射表
var_map = dict() # 变量映射表
def _proc_func(func_str: str) -> Func:
    """处理函数字符串，生成函数
    
    函数内部以逗号分隔，非函数以!开头。
    形如：!f(x,A)
    
    Args:
        func_str: str 函数字符串
    Returns:
        Func: 函数
    """
    global cnt_var, cnt_const, const_map, var_map
    func_str = func_str.strip()
    non : bool = False
    if func_str[0] == '!':
        non = True
        func_str = func_str[1:]
    name = func_str.split('(')[0]
    params_str = list(func_str.split('(')[1].split(')')[0].split(','))
    for param in params_str:
        if len(param) == 1:
            if param in var_map.keys():
                continue
            cnt_var += 1
            var_map[param] = -cnt_var
            print(f'\tvar: {param} -> {var_map[param]}')
        else:
            if param in const_map.keys():
                continue
            cnt_const += 1
            const_map[param] = cnt_const
            print(f'\tconst: {param} -> {const_map[param]}')
    params = [var_map[param] if len(param) == 1 else const_map[param] for param in params_str]
    return Func(name, non, params)

def _proc_line(line: str) -> Clause:
    """处理一行输入，分出函数，生成子句

    函数之间以空格分隔，函数内部以逗号分隔，非函数以!开头。
    形如：!f(x,A) !g(B,y)

    Args:
        line: str 输入行
    Returns:
        Clause: 子句
    """
    funcs_str = line.split(' ')
    funcs: list[Func] = []
    global var_map 
    var_map = dict() # 变量映射仅在一行内有效
    for func_str in funcs_str:
        funcs.append(_proc_func(func_str))
    return Clause(funcs)

def read_clauses(input_file: str) -> list[Clause]:
    """读取输入，生成子句集合
    
    Args:
        input_file: str 输入文件路径
    Returns:
        list[Clause]: 子句集合
    """
    clause_set : list[Clause] = []
    print("[Read&Mark]")
    with open(input_file, "r") as f:
        lines = f.readlines()
        for lnum, line in enumerate(lines):
            if len(line) == 0:
                continue
            line = line.strip()
            print(f"Proc {lnum}: {line}")
            clause_set.append(_proc_line(line))
    print()
    return clause_set