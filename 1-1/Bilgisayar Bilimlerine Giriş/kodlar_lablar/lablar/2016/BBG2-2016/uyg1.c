#include <stdio.h>

int main(void){
	//Dizideki Max Elaman� Bulma
	printf("Hello World!\n");
	printf("\n");
	int n, dizi[100], max, i;
	printf("n: ");
	scanf("%d", &n);
	for(i = 0; i < n; i++){
		printf("dizi[%d]: ", i + 1);
		scanf("%d", &dizi[i]);
	}
	max = dizi[0];
	for(i = 1; i < n; i++){
		if(dizi[i] > max)
			max = dizi[i];
	}
	printf("Maks: %d\n", max);
	
	int c;
	printf("max+1: %d\n", max + 1);
	printf("max+1,(ekrana max yazd�r�r): %d\n", max++);
	c++;
	printf("max+1: %d\n", ++max);
	
	return 0;
}
