#include <cstdlib>

void at_quick_exit_handler() {
    // This function will be called by std::quick_exit
}

int main() {
    std::at_quick_exit(at_quick_exit_handler);
    std::quick_exit(EXIT_SUCCESS);
}