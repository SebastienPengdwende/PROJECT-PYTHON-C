#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "product.h"

void init_prod(Prod *p) {
    strcpy(p->name, "");
    strcpy(p->id, "");
    strcpy(p->category, "");
    p->quantity = 0;
    p->price = 0.0;
    p->min_stock = 5;

    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    if (tm_info) {
        sprintf(p->date, "%04d-%02d-%02d", tm_info->tm_year + 1900, tm_info->tm_mon + 1, tm_info->tm_mday);
    } else {
        strcpy(p->date, "0000-00-00");
    }
}

void init_invent(Invent *inv) {
    inv->product_count = 0;
}

int is_low_stock(const Prod *p) {
    return p->quantity <= p->min_stock;
}

int count_low_stock_products(const Invent *inv) {
    int counter = 0;
    for (int i = 0; i < inv->product_count; i++) {
        if (inv->products[i].quantity <= inv->products[i].min_stock) {
            counter++;
        }
    }
    return counter;
}

void generate_unique_id(char *id, const Invent *inv) {
    int max_id = 0;
    for (int i = 0; i < inv->product_count; i++) {
        if (strncmp(inv->products[i].id, "P", 1) == 0) {
            int num = atoi(inv->products[i].id + 1);
            if (num > max_id) max_id = num;
        }
    }
    sprintf(id, "P%03d", max_id + 1);
}