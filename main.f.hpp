// Auto generated code.
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

#undef Z_F9
#undef Z_F22

#define Z_F9() (Z_F_BUILDER()<<"hello, "<<(s1+s2)).str()
#define Z_F22() [&]() { \
Z_F_BUILDER __r;\
__r<<"\n";\
for (int i=0; i<2; i++) {\
__r<<"    a is "<<(a)<<", i is "<<(i)<<".\n    a+i is "<<(a+i)<<".\n";\
}\
__r<<"b is "<<(b)<<".\n";\
cout << "123" << endl;\
__r<<""; \
return __r.str();\
}()