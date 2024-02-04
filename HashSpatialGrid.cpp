#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

class SpatialGrid {
    public:

        struct Particle {
            int id;
            vector<int> position;
        };

        vector<vector<int>> bounds;
        vector<int> dimensions;
        int cell_size;
        int num_cells;
        vector<Particle> particles;
        vector<int> pointer_array;
        vector<int> dense_array;
    

    SpatialGrid(vector<vector<int>> bounds, vector<int> dimensions, int cell_size) {
        this->bounds = bounds;
        this->dimensions = dimensions;
        this->cell_size = cell_size;
        for (int i = 0; i < max(dimensions.at(0), dimensions.at(1))+1; i++) {
            this->pointer_array.push_back(0);
        }
        this->num_cells = pointer_array.size()-1;
    }

    void Add_Particle(Particle particle){
        this->particles.push_back(particle);
    }

    int _calculateGridIndex(vector<int> position) {
        int x = position.at(0);
        int y = position.at(1);
        int xi = x / this->cell_size;
        int yi = y / this->cell_size;
        int i = (xi * (this->num_cells) + yi);
        return i;
    }

    void _solve_pointerArray() {
        for (int i = 0; i < this->particles.size(); i++) {
            int index = _calculateGridIndex(this->particles.at(i).position);
            this->pointer_array.at(index) += 1;
        }
        int prev = 0;
        for (int i = 0; i < this->pointer_array.size(); i++) {
            this->pointer_array.at(i) += prev;
            prev = this->pointer_array.at(i);
        }
        cout << "Pointer Array: ";
        for (int i = 0; i < this->pointer_array.size(); i++) {
            cout << this->pointer_array.at(i) << ", ";
        }
    }
};

int Main() {
    vector<vector<int>> bounds = {{0, 0}, {100, 100}};
    vector<int> dimensions = {100, 100};
    int cell_size = 10;
    SpatialGrid grid(bounds, dimensions, cell_size);
    SpatialGrid::Particle particle;
    particle.id = 1;
    particle.position = {10, 10};
    grid.Add_Particle(particle);
    particle.id = 2;
    particle.position = {20, 20};
    grid.Add_Particle(particle);
    particle.id = 3;
    particle.position = {30, 30};
    grid.Add_Particle(particle);
    particle.id = 4;
    particle.position = {40, 40};
    grid.Add_Particle(particle);
    particle.id = 5;
    particle.position = {50, 50};
    grid.Add_Particle(particle);
    particle.id = 6;
    particle.position = {60, 60};
    grid.Add_Particle(particle);
    particle.id = 7;
    particle.position = {70, 70};
    grid.Add_Particle(particle);
    particle.id = 8;
    particle.position = {80, 80};
    grid.Add_Particle(particle);
    particle.id = 9;
    particle.position = {90, 90};
    grid.Add_Particle(particle);
    particle.id = 10;
    particle.position = {100, 100};
    grid.Add_Particle(particle);
    grid._solve_pointerArray();
    return 0;
}