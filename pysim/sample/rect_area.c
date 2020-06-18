#include <stdio.h>
#include <string.h>
#include <stdlib.h>

float area(float h, float w)
{
    return h * w;
}


int main(int argc, char *argv[]) 
{
    int i;
    float h = 0, w = 0;
    char *pend;
    if (argc != 5) {
        printf("usage: %s --height H --width W\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    for (i = 1; i < argc; i++) {
        if(strcmp(argv[i], "--height") == 0)
            h = strtof(argv[++i], &pend);
        else if(strcmp(argv[i], "--width") == 0)
            w = strtof(argv[++i], &pend);
        else    
            printf("Unkown parameter: %s\n", argv[i]);
    }
    printf("Area(h=%.f, w=%.f) = %.f\n", h, w, area(h, w));
}