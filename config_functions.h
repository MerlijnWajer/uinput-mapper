#ifndef H_CONFIG_FUNCTIONS
#define H_CONFIG_FUNCTIONS

#define JOYSTICK_SET_OPT(opt, bit, device) \
    if (device == j) { \
        if (ioctl(js[device], bit, opt) < 0) { \
            perror("Error in JOYSTICK_SET_OPT"); \
            fprintf(stderr, "ERROR: JOYSTICK_SET_OPT for device %d, opt %s, bit: %s\n", device, #opt, #bit); \
        } else { \
            printf("JOYSTICK_SET_OPT for device %d, opt %s, bit: %s\n", device, #opt, #bit); \
        } \
    }

#define JOYSTICK_ADD_KEY(key, bit, device) \
    if (device == j) { \
        if (ioctl(js[device], bit, key) < 0) { \
            perror("Error in JOYSTICK_ADD_KEY"); \
            fprintf(stderr, "ERROR: JOYSTICK_ADD_KEY for device %d, key %s, bit: %s\n", device, #key, #bit); \
            return 1; \
        } else { \
            printf("JOYSTICK_ADD_KEY for device %d, key %s, bit: %s\n", device, #key, #bit); \
        } \
    }


#define JOYSTICK_SET_LIM(lim, val, key) \
    uidev.lim[key] = val;

#define LEGAL_VALUE(statement, macro) \
    if (statement) { \
        macro \
    }

#define KEYMAP(in_type, in_key, out_key, out_type, device, val) \
    if(e.type == in_type && e.code == in_key) {\
        je.type = out_type; \
        je.code = out_key; \
        je.value = val(e.value); \
        j = device; \
        nowrite = 0;\
    }

#endif
