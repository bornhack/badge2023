#include "shared-bindings/board/__init__.h"

STATIC const mp_rom_map_elem_t board_module_globals_table[] = {
    CIRCUITPYTHON_BOARD_DICT_STANDARD_ITEMS

    { MP_ROM_QSTR(MP_QSTR_SDA),  MP_ROM_PTR(&pin_GPIO4)  },
    { MP_ROM_QSTR(MP_QSTR_SCL),  MP_ROM_PTR(&pin_GPIO5)  },
    { MP_ROM_QSTR(MP_QSTR_IRQ),  MP_ROM_PTR(&pin_GPIO6)  },
    { MP_ROM_QSTR(MP_QSTR_VEN),  MP_ROM_PTR(&pin_GPIO7)  },
    { MP_ROM_QSTR(MP_QSTR_D1),   MP_ROM_PTR(&pin_GPIO13) },
    { MP_ROM_QSTR(MP_QSTR_D2),   MP_ROM_PTR(&pin_GPIO24) },
    { MP_ROM_QSTR(MP_QSTR_D0),   MP_ROM_PTR(&pin_GPIO25) },
    { MP_ROM_QSTR(MP_QSTR_LED),  MP_ROM_PTR(&pin_GPIO25) },
    { MP_ROM_QSTR(MP_QSTR_BTN1), MP_ROM_PTR(&pin_GPIO26) },
    { MP_ROM_QSTR(MP_QSTR_BTN2), MP_ROM_PTR(&pin_GPIO27) },

    { MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_PTR(&board_i2c_obj) },
};
MP_DEFINE_CONST_DICT(board_module_globals, board_module_globals_table);
