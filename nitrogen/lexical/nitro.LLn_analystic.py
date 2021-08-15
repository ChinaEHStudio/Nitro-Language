import re

'''
prediction_tbl_expression_sample

Vn|     id      +       *       (       )       $
——+———————————————————————————————————————————————————
E |     E->TE'                  E->TE'
E'|             E'->TE'                 E'->ε    E'->ε
T |     T->FT'                  T->FT'
T'|             T'->ε   T->*FT'         T'_>ε    T'->ε
F |     F->id                   F->(E)
'''
class LL_prediction_proc():
    pass