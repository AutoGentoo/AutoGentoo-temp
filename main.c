#include <stdio.h>
#include <tools/vector.h>

void print_bin (void* ptr, int n, size_t size) {
    int i;
    for (i=0; i != (size * n); i++) {
        int j;
        for (j=0; j<8; j++) {
            printf("%d",  !!((((char*)ptr)[i] << j) & 0x80));
        }

        if (!((i + 1) % size)) {
            printf (" ");
        }
    }
    printf("\n");
}

void print_vec(Vector* vec) {
    print_bin(vec->ptr, vec->n, vec->size);
    fflush(stdout);
}

struct __test1 {
    int a;
    int b;
};

struct __test2 {
    int a;
    int b;
    int c;
};

int main() {
    Vector* testVec = vector_new(sizeof(int), UNORDERED | REMOVE);
    print_vec(testVec);

    int el_one = 0x0;
    int el_two = 0xAAAAAAAA;

    vector_add(testVec, &el_one);
    vector_add(testVec, &el_two);
    printf("%d\n", testVec->n);
    print_vec(testVec);

    int el_1_5 = 0xFFFFFFFF;
    vector_insert(testVec, &el_1_5, 1);
    print_vec(testVec);

    vector_remove(testVec, 2);
    print_vec(testVec);
    vector_add(testVec, &el_two);
    print_vec(testVec);

    vector_free(testVec);

    return 0;
}