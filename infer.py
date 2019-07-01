from pprint import pprint
from tylmdparser import parse
from enum import Enum
import sys

class TypeInfer():
    def __init__(self, ast):
        self.__num = 0
        self.tenv = {}
        self.constraint = []
        self.typed_ast = self.__typing(ast)

    def __gensym(self):
        self.__num = self.__num + 1
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
        elif ast[0] == 'if':
            return self.__ct_if(ast)
        elif ast[0] == 'apply':
            return self.__ct_app(ast)

    # CT-Var
    # input:
    #   ast: ['var', position, str]
    # output:
    #   [type, ['var', position, str]]
    def __ct_var(self, ast):
        if ast[2] in self.tenv:
            return [self.tenv[ast[2]], ast]
        else:
            print('unexpected variable:', ast)
            raise

    # CT-True
    # input:
    #   ast: ['true', position]
    # output:
    #   ['bool' ['true', position]]
    def __ct_true(self, ast):
        return ['bool', ast]

    # CT-Zero
    # input:
    #   ast: ['zero', position]
    # output:
    #   ['int' ['zero', position]]
    def __ct_zero(self, ast):
        return ['int', ast]

    # CT-Succ
    # input:
    #   ast: ['succ', position, AST]
    # output:
    #   ['int', ['succ', position, typed AST]]
    def __ct_succ(self, ast):
        ast[2] = self.__typing(ast[2])
        self.__add_constraint(ast[2][0], 'int')
        return ['int', ast]

    # CT-Abs
    # input:
    #   ast: ['lambda', position, ['var', position, string], AST]
    # output:
    #   [[type, type], ['lambda', position, ['var', position, string], AST]]
    def __ct_abs(self, ast):
        t1 = self.__gensym()
        self.tenv[ast[2][2]] = t1
        tmp = self.__typing(ast[3])
        t2 = tmp[0]
        ast[3] = tmp
        return [[t1, t2], ast]

    # CT-If
    # input:
    #   ast: ['if', position,
    #         AST (for condition), AST (for true), AST (for false)]
    # output:
    #   [type, ['if', position, typed AST (for condition),
    #            typed AST (for true), typed AST (for false)]]
    def __ct_if(self, ast):
        ast[2] = self.__typing(ast[2]) # condition
        ast[3] = self.__typing(ast[3]) # expression when true
        ast[4] = self.__typing(ast[4]) # expression when false
        t1 = ast[2][0]
        t2 = ast[3][0]
        t3 = ast[4][0]
        self.__add_constraint(t1, 'bool')
        self.__add_constraint(t2, t3)
        return ['bool', ast]

    #
    # Implement CT-False, CT-Pred, CT-IsZero, and CT-App rules
    #

    # CT-False
    # input:
    #   ast: ['false', position]
    # output:
    #   ['bool' ['false', position]]
    def __ct_false(self, ast):
        pass # implement here

    # CT-Pred
    # input:
    #   ast: ['pred', position, AST]
    # output:
    #   ['int', ['pred', position, typed AST]]
    def __ct_pred(self, ast):
        pass # implement here

    # CT-IsZero
    # input:
    #   ast: ['iszero', position, AST]
    # output:
    #   ['bool', ['iszero', position, typed AST]]
    def __ct_iszero(self, ast):
        pass # implement here

    # CT-App
    # input:
    #   ast: ['apply', position, AST, AST]
    # output:
    #   [type, ['apply', postion, typed AST, typed AST]]
    def __ct_app(self, ast):
        pass # implement here

    def __add_constraint(self, t1, t2):
        if t1 == t2:
            return
        self.constraint.append([t1, t2])


def do_infer(exp):
    print('Expression:')
    print(exp)

    # generate AST from exp
    ast = parse(exp)
    print('AST:')
    pprint(ast)

    # infer type of AST
    ti = TypeInfer(ast)
    print('')
    print('Typed AST:')
    pprint(ti.typed_ast)

    print('')
    print('Type Constraint:')
    pprint(ti.constraint)

    print('')
    print('Type Environment:')
    pprint(ti.tenv)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print('Usage:\n  $ python %s filename' % sys.argv[0])
        quit()

    exp = open(sys.argv[1], "r").read()
    do_infer(exp)
