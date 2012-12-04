/*
 * Status:
 *
 * - Can map keys from some keyboard to keys on a joystick.
 *
 * Does not:
 * - Have a nice mapping file format / datastructures YET.
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <fcntl.h>

#include <signal.h>

#include <linux/input.h>
#include <linux/uinput.h>

#include "custom_map.h"

#define UINPUT_PATH "/dev/uinput"

/* Reverse mapping, for later use */
static const struct _key_to_str {
    char *name;
    int num;
} key_map[] = {
#define DEF_KEY(NAME) \
    {#NAME,NAME},
    #include "def_keys.h"
    {NULL, -1}
};

static int get_key_num(char* name)
{
    int i = 0;

    while (key_map[i].name) {
        if (!strcmp(key_map[i].name, name))
            return key_map[i].num;

        i++;
    }

    return -1;
}

static int js[JOYCOUNT];

/* TODO:
 * - Add file parsing / reading
 * - Add proper datastructures to keep track
 */

void free_js(int sig) {
    int j;

    (void) sig;
    for(j = 0; j < JOYCOUNT; j++) {
        printf("Freeing joystick: %d\n", j);
        if (ioctl(js[j], UI_DEV_DESTROY) < 0) {
            perror("Error freeing joystick");
        }
        close(js[j]);
    }
    exit(1);
}

int main(int argc, char** argv) {
    int j, nowrite;
    int in; /* fds */
    struct input_event e, je;
    struct uinput_user_dev uidev;


    (void)argc;
    (void)argv;

    (void)get_key_num;

    if(signal(SIGINT, free_js)) {
        printf("Atexit registration failed\n");
        return 1;
    }

    /* Open input and uinput */
    in = open(INPUT_PATH, O_RDONLY);
    if(in < 0) {
        perror("open in");
        return 1;
    }

    for(j = 0; j < JOYCOUNT; j++) {
        /* Memset because we are already setting the absmax/absmin */
        memset(&uidev, '\0', sizeof(struct uinput_user_dev));
        js[j] = open(UINPUT_PATH, O_WRONLY | O_NONBLOCK);
        if (js[j] < 0) {
            perror("open js[j]");
            return 1;
        }

        #define H_CONFIGURE_JOYSTICKS
        #include "custom_map.h"

        /* Allocate device info */
        snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "key2joy:%d", j);

        uidev.id.bustype = BUS_USB;
        uidev.id.vendor  = 0x42;
        uidev.id.product = 0xbebe;
        uidev.id.version = 1;

        if (write(js[j], &uidev, sizeof(uidev)) < 0) {
            perror("write");
            return -1;
        }

        if (ioctl(js[j], UI_DEV_CREATE)) {
            perror("ioctl create");
            return 1;
        }
    }

    /* Do it! */
    while (1) {
        if (read(in, &e, sizeof(struct input_event))) {
            printf("Event: (Type: %d, Code: %d, Value %d)\n", e.type, e.code, e.value);
        }


        memset(&je, '\0', sizeof(struct input_event));
        nowrite = 0;
        j = 0;

        /* Only catch keys and ignore auto-repeat (value == 2) */
        /* TODO: Remove this EV_KEY contraint and use it in the macro */
        if (e.type == EV_KEY && e.value != 2) {
            switch(e.code) {

            #define H_JOYMAP
            #include "custom_map.h"

            default:
                nowrite = 1;
            }
            if (nowrite == 0) {
                printf("Writing %d to %d\n", e.code, j);
                if(write(js[j], &je, sizeof(struct input_event)) < 0) {
                    perror("EV_ABS Write event");
                    return -1;
                }
            }
        }

        /* Synchronisation events */
        if (e.type == EV_SYN) {
            memset(&je, '\0', sizeof(struct input_event));
            printf("SYN event\n");

            je.type = EV_SYN;
            je.code = 0;
            je.value = 0;

            if (write(js[j], &je, sizeof(struct input_event)) < 0) {
                perror("SYN write event");
                return -1;
            }
        }
    }


}
