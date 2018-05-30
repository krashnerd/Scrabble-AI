#include <iostream>
size_t e_f_f_i_c_i_e_n_t__square(size_t n)
	{return (n==0)?0:e_f_f_i_c_i_e_n_t__square(n-1)+(2*n)-1};

int main(int argc, char** argv){
	if(argc != 2) exit(1);
	cout << e_f_f_i_c_i_e_n_t__square((size_t)(atoi(argv[1]))); << endl;
}