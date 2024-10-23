import sys
from data_structure import Clause
from read_data import read_clauses

input_file = sys.argv[1] # 输入文件路径
clause_set = read_clauses(input_file) # 子句集合
generated : list[list] = [] # 已经生成过的子句下标集，用于剪枝
substitution_count = 0 # 替换计次
unification_count = 0 # 合一计次

# 算法主体

def print_clauses():
    """打印子句集"""
    print("[Clauses]")
    for i in range(len(clause_set)):
        print(f'{i}: {clause_set[i]}')
    print()

def unification(a: Clause, b:Clause):
    """根据归结规则(Resolution)进行合一(Unification)
    
    Args:
        a: 子句a
        b: 子句b
    Returns:
        bool: 是否能够合一
        Clause: 合一后的子句
    """

    global unification_count, substitution_count
    unification_count += 1

    ia, ib = 0, 0 
    """Clause a和Clause b的Pointer"""
    ret = Clause([])
    """合一后的子句"""

    # Two-Pointer：寻找可归结的函数对
    fl = 0 # 是否找到
    for i in range(len(a.funcs)):
        for j in range(len(b.funcs)):
            if a.funcs[i].resolutable(b.funcs[j]): # 如果两个函数可归结
                ia, ib = i, j
                fl = 1
                break
        if fl:
            break 
    if not fl: # 未找到可归结的函数对，无法合并
        return False, ret
    
    # Substitution：找到需要替换的变量，进行替换
    fa, fb = a.funcs[ia], b.funcs[ib]
    chg = dict()  # 替换表
    for i in range(len(fa.params)): 
        if fa.params[i] * fb.params[i] < 0: # 一个是变量，一个是常量，进行Substitution
            if fa.params[i] > 0:
                chg[fb.params[i]] = fa.params[i]
                print(f"Substitution: {fb.params[i]} -> {fa.params[i]}")
            else:
                chg[fa.params[i]] = fb.params[i]
                print(f"Substitution: {fa.params[i]} -> {fb.params[i]}")
        elif fa.params[i] < 0 and fb.params[i] < 0 and fa.params[i] != fb.params[i]: # 两个都是变量
            chg[fa.params[i]] = fb.params[i]
            chg[fb.params[i]] = fb.params[i]
            print(f"Substitution: {fa.params[i]} -> {fb.params[i]}")

    # Merge：将a中的其他函数加入到新的子句中
    for i in range(len(a.funcs)): 
        func = a.funcs[i]
        if i == ia:
            continue
        for idx, x in enumerate(func.params):
            if x < 0 and chg.get(x, 0) != 0:
                substitution_count += 1
                func.params[idx] = chg[x]
        ret.funcs.append(func)

    # Merge：将b中的其他函数加入到新的子句中
    for i in range(len(b.funcs)): 
        func = b.funcs[i]
        if i == ib:
            continue
        for idx, x in enumerate(func.params):
            if x < 0 and chg.get(x, 0) != 0:
                substitution_count += 1
                func.params[idx] = chg[x]
        ret.funcs.append(func)

    # Adjust：消除重复元素、相反元素
    ret.adjust()
    
    return True, ret

def dfs(cur_clause:Clause, vis:list):
    """深度优先搜索，合并子句

    Args:
        cl: 当前子句
        vis: 已访问的点集
    """
    global generated
    if sorted(vis) in generated: # 剪枝，避免重复搜索
        print(f"Skipped: \t{sorted(vis)}")
        return
    global clause_set
    for idx, clause in enumerate(clause_set):
        if idx in vis:
            continue
        fl, new_clause = unification(cur_clause, clause)
        if fl: # 如果可以合并
            vis.append(idx)
            print(f"Merge: \t{sorted(vis)} => {new_clause}")
            if len(new_clause.funcs) == 0: # 如果合并后的子句为空，证明已经推导出矛盾，原命题成立
                print()
                print("[Result] Accepted")
                print(f"Substitution Count: {substitution_count}")
                print(f"Unification Count: {unification_count}")
                exit(0)
            dfs(new_clause, vis) # 递归搜索
            vis.remove(idx)
        else:
            print(f"Failed Merge: {idx} into {sorted(vis)}")
    generated.append(sorted(vis))

def proc():
    print("[Process]")
    global clause_set
    for idx,clause in enumerate(clause_set): # 枚举从每一个子句开始DFS
        dfs(clause, [idx])
    print()

if __name__=="__main__":
    print_clauses()
    proc()
    print("[Result] Wrong")
    print(f"Substitution Count: {substitution_count}")
    print(f"Unification Count: {unification_count}")