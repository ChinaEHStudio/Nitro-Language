import re

LEX_BRAKE=0X00
LEX_OP=0X01
LEX_KW=0X02
LEX_CUSTOM=0X03
#asndjhaifhsugfusavfiuzgdsifhbsddfh
LEX_COMMA=0X0000
LEX_S_LB=0X0001
LEX_S_RB=0X0002
LEX_M_LB=0X0003
LEX_M_RB=0X0004
LEX_L_LB=0X0005
LEX_L_RB=0X0006
LEX_SPL=0X0007
LEX_ADD=0X0010
LEX_MIN=0X0011
LEX_MUL=0X0012
LEX_SUB=0X0013
LEX_MOD=0X0014
LEX_VAL=0X0015
LEX_NOT=0X0016
LEX_EQL=0X0017
LEX_SMALL=0X0018
LEX_BIG=0X0019
LEX_SMALLOREQL=0X001A
LEX_BIGOREQUAL=0X001B
LEX_NOTEQUAL=0X001C
LEX_ANDAND=0X001D
LEX_OROR=0X001E
LEX_XOR=0X001F
LEX_ADDADD=0X0020
LEX_MINMIN=0X0021
LEX_ADDEQL=0X0022
LEX_MINEQL=0X0023
LEX_NAMESP=0X0024
LEX_QM_NAMESP=0X0025
LEX_DOT=0X0026
LEX_IF=0X0030
LEX_ELSE=0X0031
LEX_ELIF=0X0032
LEX_FOR=0X0033
LEX_WHILE=0X0034
LEX_FOREACH=0X0035
LEX_BREAK=0X0036
LEX_CONTINUE=0X0037
LEX_TRY=0X0038
LEX_EXCEPT=0X0039
LEX_FINALLY=0X003A
LEX_INT=0X0040
LEX_STRING=0X0041
LEX_FLOAT=0X0042
LEX_DOUBLE=0X0043
LEX_VOID=0X0044
LEX_AUTO=0X0045
LEX_BOOL=0X0046

LEX_FUNCTION=0X0050
LEX_NEW=0X0051
LEX_RETURN=0X0052

LEX_PUBLIC=0X0060
LEX_PRIVATE=0X0061
LEX_REG=0X0062

LEX_NONTOKEN=0x01ff#包括变量名，数字，等等
LEX_USERDEF_TYPE=0X02ff

class lexical_processor():
    '''
    文法：G=(Vt,Vn,P,S)
    terminal symbols(Vt) for language.
    '''
    brakes=[',','(',')','[',']','{','}',';']
    operators=['+','-','*','/','%','=',#算术运算符，其中*也可为地址操作。多义性须在后续处理中消除。
        '&',#地址
        '!','<','>','<=','>=','!=','&&','||','^',#逻辑运算符
        '++','--','+=','-=',#特殊算术运算符
        '::','?:','.'#其它
        ]
    #关键字
    kw=[
        'if','else','elif','for','while','foreach','break','continue','try','except','finally',
        'int','string','float','double','void','auto','bool','function','const','new',
        'public','private','reg','new','return'
    ]
    source_code=str()
    src_code_list=[]
    token=[]

    nontoken_symbols_list=[]
    #defined_symbols_list=[]
    sorted_token=[]#这玩意被我搞成了Vt和Vn的并集，算了不管力
    def __init__(self,src_code):
        src=self.post_process(src_code)
        self.source_code=src
        tmp_src_code_list=list(src)#临时的
        for ml in ('',' ','\n','\t'):#去掉空字符。其实可以用regex的，但是我懒。
            while ml in tmp_src_code_list:tmp_src_code_list.remove(ml)
        self.src_code_list=tmp_src_code_list
        self.token=self.tokenize(self.src_code_list)
        for t in self.token:
            if self.sort_token_type(t):
                self.sorted_token.append(self.token_to_num(t),t)#将token按照 类型, 内容分类
            else:
                self.sorted_token.append(LEX_NONTOKEN,t)#得专门弄个啥东西处理变量，太复杂了
                self.nontoken_symbols_list.append(t)#不过也可以把这些东西留到后面处理，不管了，就这样吧。
                '''if (not t in self.kw)\
                and (not t in self.brakes)\
                and (not t in self.operators):#暂时没法处理字符串 现在写了
                '''
            
        
    def tokenize(self,src_list):
        dbl_operator=False
        count=0
        max_count=len(src_list)-1
        non_token_tmp=str()
        token=[]
        while count<=max_count:
            mark=src_list[count]
            mark_next=(src_list[count+1] if count+1<=max_count else '')
            probable_dbl_op=mark+mark_next
            if probable_dbl_op in self.operators:
                if non_token_tmp != '':token.append(non_token_tmp.strip())
                token.append(probable_dbl_op)
                non_token_tmp=''
                count+=2
                continue
            elif mark in self.operators or mark in self.brakes:
                if non_token_tmp!='':token.append(non_token_tmp.strip())
                token.append(mark)
                non_token_tmp=''
                count+=1
                continue
            else:
                non_token_tmp+=mark
                count+=1
        if non_token_tmp != '':token.append(non_token_tmp.strip())

    def sort_token_type(self,token):
        if not token in self.brakes and not token in self.kw and not token in self.operators:return False#典型的屎山，什么时候改一下 
        else: return True

    def post_process(self,src_code):
        regex_note=r'(\/\/.*)' #双/型注释
        src_code=re.sub(regex_note,'',src_code)
        regex_string=r'\"(\S*)\"' #单行字符串，内部嵌有的引号好像不会被识别
        strings=re.findall(regex_string,src_code)
        count=0
        strings_predef='' 
        while count<=len(strings):
            src_code.replace('"'+strings[count]+'"','__nitro_runtime_str_'+str(count),1)
            strings_predef+='#predef string __nitro_runtime_str_'+str(count)+' '+'"'+strings[count]+'"'+'\n'#需要指出的是，predef可以用来定义新的变量类型
            count+=1
        return strings_predef+src_code

    def token_to_num(self,token):
        table={
            ',':LEX_COMMA,
            '(':LEX_S_LB,
            ')':LEX_S_RB,
            '[':LEX_M_LB,
            ']':LEX_M_RB,
            '{':LEX_L_LB,
            '}':LEX_L_RB,
            ';':LEX_SPL,
            '+':LEX_ADD,
            '-':LEX_MIN,
            '*':LEX_MUL,
            '/':LEX_SUB,
            '%':LEX_MOD,
            '=':LEX_VAL,
            '&':LEX_NOT,
            '!':LEX_EQL,
            '<':LEX_SMALL,
            '>':LEX_BIG,
            '<=':LEX_SMALLOREQL,
            '>=':LEX_BIGOREQUAL,
            '!=':LEX_NOTEQUAL,
            '&&':LEX_ANDAND,
            '||':LEX_OROR,
            '^':LEX_XOR,
            '++':LEX_ADDADD,
            '--':LEX_MINMIN,
            '+=':LEX_ADDEQL,
            '-=':LEX_MINEQL,
            '::':LEX_NAMESP,
            '?:':LEX_QM_NAMESP,
            '.':LEX_DOT,
            'if':LEX_IF,
            'else':LEX_ELSE,
            'elif':LEX_ELIF,
            'for':LEX_FOR,
            'while':LEX_WHILE,
            'foreach':LEX_FOREACH,
            'break':LEX_BREAK,
            'continue':LEX_CONTINUE,
            'try':LEX_TRY,
            'except':LEX_EXCEPT,
            'finally':LEX_FINALLY,
            'int':LEX_INT,
            'string':LEX_STRING,
            'float':LEX_FLOAT,
            'double':LEX_DOUBLE,
            'void':LEX_VOID,
            'auto':LEX_AUTO,
            'bool':LEX_BOOL,
            'function':LEX_FUNCTION,
            'new':LEX_NEW,
            'return':LEX_RETURN,
            'public':LEX_PUBLIC,
            'private':LEX_PRIVATE,
            'reg':LEX_REG,
            #'type':LEX_USERDEF_TYPE#用户自定义类型
        } 
        return table[token]