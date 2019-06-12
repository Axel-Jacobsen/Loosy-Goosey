#include <stdio.h>
#include <math.h>

float dist(float x1, float y1, float x2, float y2)
{
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

int main(void)
{
    printf("%f\n", dist(0,0,3,4));
}