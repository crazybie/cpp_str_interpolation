# cpp_str_interpolation
super simple but powerfull C++ string interpolation and template engine.

## usage:
```c++
void test1() {
  string s1 = "world", s2 = "!";
  cout << _F("hello, {s1+s2}") << endl;
}

void test2() {
  int a = 1;
  float b = 2.3f;
  cout << _F(R"(
`for (int i=0; i<2; i++) {`
    a is {a}, i is {i}.
    a+i is {a+i}.
`}`
b is {b}.
`cout << "123" << endl;`
)") << endl;
}
```
