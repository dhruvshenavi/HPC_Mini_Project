#include <iostream>
#include <cstring>
#include <cctype>
#include <omp.h>

extern "C" {

int count_matches(const char** lines, int n, const char* keyword) {
    int count = 0;

    // convert keyword to lowercase
    char key_lower[100];
    int i = 0;
    while (keyword[i] != '\0') {
        key_lower[i] = tolower(keyword[i]);
        i++;
    }
    key_lower[i] = '\0';

    #pragma omp parallel for reduction(+:count)
    for (int i = 0; i < n; i++) {

        char cleaned[1000];
        int j = 0;

        // clean the line
        for (int k = 0; lines[i][k] != '\0'; k++) {
            char c = lines[i][k];

            if (isalnum(c) || c == ' ') {
                cleaned[j] = tolower(c);
                j++;
            }
        }
        cleaned[j] = '\0';

        // check keyword (simple search)
        if (strstr(cleaned, key_lower) != NULL) {
            count++;
        }
    }

    return count;
}

}