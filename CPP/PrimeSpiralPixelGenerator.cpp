#include <iostream>
#include <string>
#include <algorithm>
#include <cstdint>
#include <cmath>
#include <fstream> // For file I/O

// this program generates an array of pixel colors for a prime spiral
// central pixel is 1, then the program tries to go forwards and always tries to go counter clockwise
// if it can't go counter clockwise, it goes forwards.
// each time it goes forwards, it increments the value placed by 1
// if the value is prime the pixel is given a color based on its position, else it is white

using namespace std;

bool isPrime(int val){
    if (val == 1){
        return false;
    }
    if (val == 2){
        return true;
    }
    if (val%2 == 0){
        return false;
    }
    for (int i = 3; i*i <= val; i+=2){
        if (val%i == 0){
            return false;
        }
    }
    return true;
}

bool isEven(int val){
    return val%2 == 0;
}

bool isSquare(int val){
    int root = sqrt(val);
    return root*root == val;
}

bool isPerfect(int val) {
    if (val == 1) return false; // 1 is not a perfect number

    int sum = 1; // Start sum at 1 since 1 is a divisor of all numbers
    int sqrtVal = sqrt(val);

    for (int i = 2; i <= sqrtVal; i++) {
        if (val % i == 0) {
            sum += i;
            if (i != val / i) { // Avoid adding the square root twice for perfect squares
                sum += val / i;
            }
        }
    }

    return sum == val;
}

bool isFibonacci(int val){
    return isSquare(5*val*val + 4) || isSquare(5*val*val - 4);
}

int main(){
    int width = 10001;
    int height = 10001;
    // array of 24 bits
    uint32_t* pixels = new uint32_t[width * height];
    uint32_t* cells = new uint32_t[width * height];

    for (int i = 0; i < width*height; i++){
        pixels[i] = 0;
        cells[i] = 0;
    }
    int i = (width*height)/2;
    int di = 1;
    int dj = -width;
    int n = 1;
    while (n <= (width*height)){
        cells[i] = n;
        n++;
        i = i + di;
        int leftcell = cells[i + dj];
        if (leftcell == 0){
            di = dj;
            if (dj == 1){
                dj = -width;
            }else if (dj == -width) {
                dj = -1;
            }else if (dj == -1){
                dj = width;
            }else {
                dj = 1;
            }
        }
    }

    cout << "Generating pixel data..." << endl;
    
    for (int i = 0; i < width*height; i++){
        int cell = cells[i];
        if (isPrime(cell)){
            int x = cell%width;
            int y = cell/width;
            int x_factor = 255/width;
            int y_factor = 255/height;
            int g_factor = 255/(width*height);
            int r = min(x*(x_factor), 255);
            int g = min((x*y)*g_factor, 255);
            int b = min(y*y_factor, 255);
            r = r<<16;
            g = g<<8;
            uint32_t rgb = r+g+b;
            pixels[i] = rgb;
        }else{
            uint32_t rgb = 16777215;
            pixels[i] = rgb;
        }
    }

    cout << "Writing to file..." << endl;

    std::ofstream file("PrimeSpiralPixelData.txt");
    if (file.is_open()) {
        for (int i = 0; i < width*height; i++) {
            file << pixels[i];
            if (i+1<width*height){
                file << ",";
            }
        }
        file.close(); // Don't forget to close the file
    } else {
        std::cerr << "Unable to open file for writing." << std::endl;
    }

    delete[] pixels;
    delete[] cells;

    return 0;
}