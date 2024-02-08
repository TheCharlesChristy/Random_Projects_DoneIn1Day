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
        int num_cells[2];
        vector<Particle> particles;
        vector<int> pointer_array;
        vector<int> dense_array;
    

    SpatialGrid(vector<vector<int>> bounds, vector<int> dimensions, int cell_size) {
        this->bounds = bounds;
        this->dimensions = dimensions;
        this->cell_size = cell_size;
        this->num_cells[0] = (dimensions.at(0)) / cell_size;
        this->num_cells[1] = (dimensions.at(1)) / cell_size;
        for (int i = 0; i < (num_cells[0]*num_cells[1]) + 1; i++) {
            this->pointer_array.push_back(0);
        }
    }

    void Add_Particle(Particle particle){
        this->particles.push_back(particle);
        this->dense_array.push_back(0);
    }

    int _calculateGridIndex(vector<int> position) {
        int x = position.at(0);
        int y = position.at(1);
        int xi = x / cell_size;
        int yi = y / cell_size;
        int i = (xi * (num_cells[1]) + yi);
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
    }

    void _solve_denseArray() {
        _solve_pointerArray();
        for (int i = 0; i < this->particles.size(); i++) {
            int index = _calculateGridIndex(this->particles.at(i).position);
            pointer_array.at(index) -= 1;
            dense_array.at(pointer_array.at(index)) = particles.at(i).id;
        }
    }

    vector<int> _solve_nearbyCellIds(int index) {
        int left_cellid = index - num_cells[1];
        int right_cellid = index + num_cells[1];

        int temp[9] = {left_cellid-1, left_cellid, left_cellid+1, index-1, index, index+1, right_cellid-1, right_cellid, right_cellid+1};
        
        vector<int> nearbyCellIds;

        for (int i = 0; i < 9; i++) {
            if (temp[i] >= 0 && temp[i] < (num_cells[0]*num_cells[1])) {
                nearbyCellIds.push_back(temp[i]);
            }
        }
        return nearbyCellIds;
    }

    vector<int> get_particlesInCell(int index) {
        int densei = pointer_array.at(index);
        int amount_of_particles = pointer_array.at(index + 1) - densei;
        vector<int> particlesInCell;
        for (int i = 0; i < amount_of_particles; i++) {
            particlesInCell.push_back(dense_array.at(densei + i));
        }
        return particlesInCell;
    }

    vector<int> _solve_nearbyParticleIds(vector<int> position) {
        int index = _calculateGridIndex(position);
        vector<int> nearbyCellIds = _solve_nearbyCellIds(index);
        vector<int> nearbyParticleIds;
        for (int i = 0; i < nearbyCellIds.size(); i++) {
            vector<int> particlesInCell = get_particlesInCell(nearbyCellIds.at(i));
            for (int j = 0; j < particlesInCell.size(); j++) {
                nearbyParticleIds.push_back(particlesInCell.at(j));
            }
        }
        return nearbyParticleIds;
    }

    void _reset_arrays () {
        for (int i = 0; i < this->pointer_array.size(); i++) {
            this->pointer_array.at(i) = 0;
        }
        for (int i = 0; i < this->dense_array.size(); i++) {
            this->dense_array.at(i) = 0;
        }
    }

    void update () {
        _reset_arrays();
        _solve_denseArray();
    }

    vector<vector<int>> get_allNearbyParticles() {
        vector<vector<int>> nearbyParticles;
        for (int i = 0; i < this->particles.size(); i++) {
            vector<int> nearbyParticleIds = _solve_nearbyParticleIds(this->particles.at(i).position);
            nearbyParticles.push_back(nearbyParticleIds);
        }
        return nearbyParticles;
    }
};

int main() {
    vector<vector<int>> bounds = {{0, 0}, {100, 80}};
    vector<int> dimensions = {100, 80};
    int cell_size = 20;
    SpatialGrid grid(bounds, dimensions, cell_size);
    SpatialGrid::Particle particle;
    particle.id = 1;
    particle.position = {30, 37};
    grid.Add_Particle(particle);
    particle.id = 2;
    particle.position = {55, 72};
    grid.Add_Particle(particle);
    particle.id = 3;
    particle.position = {61, 22};
    grid.Add_Particle(particle);
    particle.id = 4;
    particle.position = {44, 64};
    grid.Add_Particle(particle);
    particle.id = 5;
    particle.position = {22, 22};
    grid.Add_Particle(particle);

    grid.update();

    vector<vector<int>> nearbyParticles = grid.get_allNearbyParticles();
    for (int i = 0; i < nearbyParticles.size(); i++) {
        cout << "Particle " << i+1 << " is nearby to: ";
        for (int j = 0; j < nearbyParticles.at(i).size(); j++) {
            cout << nearbyParticles.at(i).at(j) << " ";
        }
        cout << endl;
    }
    return 0;
}