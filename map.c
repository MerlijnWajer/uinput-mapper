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

#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"
/*#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"*/
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

static int js[2];

/* TODO:
 * - Add file parsing / reading
 * - Add proper datastructures to keep track
 */

void free_js(int sig) {
    int j;
    for(j = 0; j < 2; j++) {
        printf("Freeing joystick: %d\n", j);
        if (ioctl(js[j], UI_DEV_DESTROY) < 0) {
            perror("Error freeing joystick");
        }
        close(js[j]);
    }
    exit(1);
}

int main(int argc, char** argv) {
    int i, j, nowrite;
    int in; /* fds */
    struct input_event e, je;
    struct uinput_user_dev uidev;

    int abskeyevs[] = {
        ABS_HAT0X,
        ABS_HAT0Y,
        0
    };

    int evkeys[] = {
        BTN_JOYSTICK, /* We need this to show up as Joystick */
        BTN_0,
        BTN_1,
        BTN_2,
        BTN_3,
        0
    };

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



    for(j = 0; j < 2; j++) {
        /* Memset because we are already setting the absmax/absmin */
        memset(&uidev, '\0', sizeof(struct uinput_user_dev));
        js[j] = open(UINPUT_PATH, O_WRONLY | O_NONBLOCK);
        if (js[j] < 0) {
            perror("open js[j]");
            return 1;
        }

        /* Register device opts */
        if (ioctl(js[j], UI_SET_EVBIT, EV_ABS) < 0) {
            perror("ioctl EV_ABS");
            return 1;
        }

        if (ioctl(js[j], UI_SET_EVBIT, EV_KEY) < 0) {
            perror("ioctl EV_KEY");
            return 1;
        }

        /* Every ``button'' needs to be registered */
        i = 0;
        while(abskeyevs[i] != 0) {
            if (ioctl(js[j], UI_SET_ABSBIT, abskeyevs[i]) < 0) {
                perror("ioctl dynamic");
                return 1;
            }
            uidev.absmax[abskeyevs[i]] = 1;
            uidev.absmin[abskeyevs[i]] = -1;
            i++;
        }

        i = 0;
        while(evkeys[i] != 0) {
            if (ioctl(js[j], UI_SET_KEYBIT, evkeys[i]) < 0) {
                perror("ioctl dynamic 2");
                return 1;
            }
            i++;
        }


        /* Allocate device info */
        snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "key2joy:1");

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
        if (e.type == EV_KEY && e.value != 2) {
            switch(e.code) {

            #include "custom_map.h"

            default:
                nowrite = 1;
            }
            if (nowrite == 0) {
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
