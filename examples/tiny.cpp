template <typename T>
struct Identity
{
    typedef T Type;
};

const unsigned int & bar() { return 5; }

const inline Identity<int>::Type &
foo(int y = bar())
{
    static int i = 0;
    return i;
}
