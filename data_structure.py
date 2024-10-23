"""数据结构模块

定义了算法所需的数据结构。

Classes:
    Func: 函数类
    Clause: 子句类
"""

class Func:
    """函数类
    
    Attributes:
        name: str 函数名
        non: bool 是否为非
        params: list[int] 参数列表，小于0表示变量、大于0表示常量
    
        __eq__: 判断两个函数是否完全相同
        resolutable: 判断两个函数是否可归结
        __xor__: 判断两个函数是否完全相反
        __repr__: 返回函数的字符串表示
    """
    def __init__(self, name: str, non: bool=False, params: list[int]=[]):
        """初始化函数
        
        Args:
            name: 函数名
            non: 是否为非
            params: 参数列表，小于0表示变量、大于0表示常量
        """
        self.name = name
        self.non = non
        self.params = params
    
    def __eq__(self, other):
        """判断两个函数是否完全相同"""
        return (self.name == other.name) and (self.non == other.non) and (self.params == other.params)
    
    def resolutable(self, other) -> bool:
        """判断两个函数是否可归结"""
        if self.name != other.name or self.non == other.non or len(self.params) != len(other.params):
            return False
        sz = len(self.params)
        for i in range(sz):
            if self.params[i] * other.params[i] > 0 and self.params[i] != other.params[i] and self.params[i] > 0: # 两个不相等的常量
                return False
        return True
    
    def __xor__(self, other) -> bool:
        """判断两个函数是否完全相反"""
        if self.name != other.name or self.non == other.non or len(self.params) != len(other.params):
            return False
        sz = len(self.params)
        for i in range(sz):
            if self.params[i] * other.params[i] < 0: # 一个是变量，一个是常量
                return False
            if self.params[i] > 0 and self.params[i] != other.params[i]: # 两个不相等的常量
                return False
        return True

    def __repr__(self) -> str:
        """返回函数的字符串表示"""
        non = '!' if self.non else '' 
        return non + self.name + '(' + ','.join(map(str, self.params)) + ')'
    
class Clause:
    """子句类
    
    Attributes:
        funcs: list[Func] 函数列表

        __repr__: 返回子句的字符串表示
        adjust: 消除重复元素、相反元素
    """
    def __init__(self, funcs: list[Func]):
        self.funcs = funcs
    
    def __repr__(self) -> str:
        """返回子句的字符串表示"""
        return ' '.join(map(str, self.funcs))
    
    def adjust(self):
        """消除重复元素、相反元素"""
        for i in range(len(self.funcs)):
            for j in range(i + 1, len(self.funcs)):
                if self.funcs[i] == self.funcs[j]:
                    self.funcs.remove(self.funcs[j])
                    self.adjust()
                    return
                if self.funcs[i]^self.funcs[j]:
                    self.funcs.remove(self.funcs[j])
                    self.funcs.remove(self.funcs[i])
                    self.adjust()
                    return
