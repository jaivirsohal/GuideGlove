#include <stdio.h>
#include <pigpiod_if2.h>
#include <unistd.h>    // for usleep()

#define TRIG_PIN 21
#define ECHO_PIN 20
#define OUTPUT_FILENAME "distances.txt"

int main(void) {
    // connect to local pigpiod daemon
    int pi = pigpio_start(NULL, NULL);
    if (pi < 0) {
        fprintf(stderr, "Failed to connect to pigpiod daemon\n");
        return 1;
    }

    // configure pins
    set_mode(pi, TRIG_PIN, PI_OUTPUT);
    set_mode(pi, ECHO_PIN, PI_INPUT);
    gpio_write(pi, TRIG_PIN, 0);
    sleep(1);  // let sensor settle

    printf("Writing distance data to %s. Press Ctrl+C to stop.\n", OUTPUT_FILENAME);

    while (1) {
        gpio_write(pi, TRIG_PIN, 1);
        usleep(10);
        gpio_write(pi, TRIG_PIN, 0);

        unsigned int startTick, endTick;

        double timeout_start = time_time();
        while (gpio_read(pi, ECHO_PIN) == 0) {
            if (time_time() - timeout_start > 0.1) { startTick = 0; break; }
        }
        startTick = get_current_tick(pi);

        if (startTick != 0) { // Only proceed if we got a start tick
             timeout_start = time_time();
             while (gpio_read(pi, ECHO_PIN) == 1) {
                if (time_time() - timeout_start > 0.1) { endTick = 0; break; }
             }
             endTick = get_current_tick(pi);
        } else {
            endTick = 0;
        }
        
        // Open the file in "write" mode ('w'). This overwrites the file every time.
        FILE *file_ptr = fopen(OUTPUT_FILENAME, "w");

        if (file_ptr == NULL) {
            fprintf(stderr, "Error: Could not open file %s for writing.\n", OUTPUT_FILENAME);
        } else {
            if (endTick > startTick) {
                float pulse_us = (float)(endTick - startTick);
                float dist_cm  = (pulse_us / 1e6f) * 17150.0f;
                // Write the formatted string to the file instead of the console
                fprintf(file_ptr, "%.2f", dist_cm);
            } else {
                fprintf(file_ptr, "-1.0");
            }
            fclose(file_ptr);
        }

        usleep(50000);  // 0.05s between measurements
    }

    pigpio_stop(pi);
    return 0;
}
