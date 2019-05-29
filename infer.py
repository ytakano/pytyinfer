from parser import parse
from enum import Enum

class TypeInfer():
    def __init__(self, ast):
        self.__num = 0
        self.tenv = {}
        self.constraint = []
        self.result = self.__typing(ast)

    def __mksym(self):
        tnum = self.__num + 1
        return 'T' + str(self.__num)

    def __typing(self, ast):
        if ast[0] == 'true':
            return self.__ct_true(ast)
        elif ast[0] == 'false':
            return self.__ct_false(ast)
        elif ast[0] == 'zero':
            return self.__ct_zero(ast)
        elif ast[0] == 'succ':
            return self.__ct_succ(ast)
        elif ast[0] == 'pred':
            return self.__ct_pred(ast)
        elif ast[0] == 'iszero':
            return self.__ct_iszero(ast)
        elif ast[0] == 'lambda':
            return self.__ct_abs(ast)
        elif ast[0] == 'var':
            return self.__ct_var(ast)

    # CT-Var
    # input:
    #   ast: ['var', position, str]
    # output:
    #   [type variable, ['var', position, str]]
    def __ct_var(self, ast):
        if ast[2] in self.tenv:
            return [self.tenv[ast[2]], ast]
        else:
            print('unexpected variable:', ast)
            raise

    # CT-True
    def __ct_true(self, ast):
        return ['bool', ast]

    # CT-False
    def __ct_false(self, ast):
        return ['bool', ast]

    # CT-Zero
    def __ct_zero(self, ast):
        return ['int', ast]

    # CT-Succ
    # input:
    #   ast: ['succ', position, AST]
    # output:
    #   ['int', ['succ', position, typed AST]]
    def __ct_succ(self, ast):
        ast[2] = self.__typing(ast[2])
        self.constraint.append((ast[2][0], 'int'))
        return ['int', ast]

    # CT-Pred
    # input:
    #   ast: ['pred', position, AST]
    # output:
    #   ['int', ['pred', position, typed AST]]
    def __ct_pred(self, ast):
        ast[2] = self.__typing(ast[2])
        self.constraint.append((ast[2][0], 'int'))
        return ['int', ast]

    # CT-IsZero
    # input:
    #   ast: ['iszero', position, AST]
    # output:
    #   ['bool', ['iszero', position, typed AST]]
    def __ct_iszero(self, ast):
        ast[2] = self.__typing(ast[2])
        self.constraint.append((ast[2][0], 'int'))
        return ['bool', ast]

    # CT-Abs
    # input:
    #   ast: ['lambda', position, ['var', position, string], AST]
    # output:
    #   [(type variable, type variable),
    #    ['lambda', position, ['var', position, string], AST]]
    def __ct_abs(self, ast):
        t1 = self.__mksym()
        self.tenv[ast[2][2]] = t1
        tmp = self.__typing(ast[3])
        t2 = tmp[0]
        ast[3] = tmp
        return [(t1, t2), ast]

d1 = '''
fun x { iszero(x) }
'''
#fun x { iszero(pred(succ(succ(false)))) }

ast = parse(d1)
print(ast)

t = TypeInfer(ast)
print(t.result)
print(t.constraint)

# d2 = '''
# fun x {
#     if x then succ(0) else succ(succ(0))
# } (true)'''

# print(parse(d2))
