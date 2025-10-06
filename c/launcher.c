#include <stdio.h>
#include <stdlib.h> // For system()
#include <signal.h> // For signal handling
#include <unistd.h> // For pause()

// This function will run when you press Ctrl+C
void handle_shutdown(int signum) {
    printf("\nShutting down C processes...\n");
    
    // Kill the background processes by name
    system("killall sensor_file_writer");
    system("killall run");
    
    printf("Cleanup complete.\n");
    exit(0);
}

int main() {
    // Intercept the Ctrl+C signal (SIGINT)
    signal(SIGINT, handle_shutdown);

    printf("Starting GuideGlove C components in the background...\n");

    system("/home/glove/GuideGlove/c/sensor_file_writer &");
    system("/home/glove/GuideGlove/c/run &");

    printf("C components are running. This launcher will wait...\n");
    printf("Press Ctrl+C to stop all C components.\n");
    
    // The pause() function simply waits until a signal is received.
    // This keeps the launcher running without using CPU.
    pause();

    return 0; // This line is never reached
}
