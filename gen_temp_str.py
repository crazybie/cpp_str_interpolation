'''
auto w = "world"; 
std::cout << _F("hello, {w}");
'''

import sys, re, os

f = sys.argv[1]
all = open(f).read()
gen_f = '.'.join(f.split('.')[:-1])+'.f.hpp'

############
# include the gen file
base = os.path.basename(gen_f)
if not re.search(fr'#include "\./{re.escape(base)}"', all):
    last_include = re.finditer(fr'#include.*\n', all)
    if last_include:
        p = next(last_include).end()
        all = all[:p]+ f'\n#include "./{base}"\n' + all[p:]
        open(f, 'w').write(all)


###########
# parse
line_ends = [i.end() for i in re.finditer(".*\n", all)]
s = []
for m in re.finditer(r'(_F\("(.*?)"\))|(_F\(R"\((.*?)\)"\))', all, re.DOTALL|re.M):
    t = m.group(2)
    if t:
        g = 2
    else:
        t = m.group(4)
        g = 4
    lno = [idx + 1 for idx, l in enumerate(line_ends) if l>m.end(g)][0]
    s.append([lno, t, g])    
    print([idx + 1 for idx, l in enumerate(line_ends) if l>m.start(g)][0])
    
##########
# generate

o = '''// Auto generated code.
#pragma once

#ifndef Z_F_BUILDER
#include <sstream>
#define Z_F_BUILDER std::ostringstream
#endif

#ifndef Z_F_CAT
#define Z_F_CAT(A,B) Z_F_CAT2(A,B)
#define Z_F_CAT2(A,B) A##B
#define _F(A) Z_F_CAT(Z_F,__LINE__)()
#endif

'''
for lno, i, g in s:
    o += f'#undef Z_F{lno}\n'
    
o += "\n"
for lno, i, g in s:

    # single line
    if g == 2:
        o += f'#define Z_F{lno}() (Z_F_BUILDER()'        
        for j in re.split(r'(\{.*?\})', i):
            if not j: continue
            o += '<<'
            if '{' in j:
                o += re.sub(r'\{(.*?)\}', r'(\1)', j)
            else:
                o += '"' + j.replace("\n","\\n") + '"'        
        o += ').str()\n'
        
    # multiple lines
    if g == 4:
        o += f'#define Z_F{lno}() [&]() {{ \\\n'
        o += 'Z_F_BUILDER __r;\\\n'
        st = 'normal'
        pre = 'newline'
        for t in i:
            if st=='normal':
                if t == '{':
                    if pre=='normal':
                        o+='"'
                    o+= '<<('
                    pre=st
                    st='exp'
                elif t == '`':
                    if pre=='normal':
                        o+='";\\\n'
                    pre=st
                    st='raw'
                else:
                    if pre=='raw':
                        if t=='\n':
                            o+='\\\n'
                            o+='__r<<"'
                            pre=st
                    elif pre=='exp':
                        if t=='\n':
                            o+='<<"\\n";\\\n'
                            pre='newline'
                        else:
                            o+='<<"'+t
                            pre=st
                    else: 
                        if pre=='newline':
                            o+='__r<<"'
                            pre=st                    
                        if t=='\n':
                            o+='\\n'
                        else:
                            o+=t
            elif st=='exp':
                if t == '}':
                    o+=')'
                    pre=st
                    st='normal'
                else:
                    o+=t
            elif st=='raw':
                if t=='`':
                    pre=st
                    st='normal'
                else:
                    o+=t
        if pre=='normal':
            o+='"'
        o+='; \\\nreturn __r.str();\\\n'
        o+='}()'
            

open(gen_f, 'w').write(o)



    