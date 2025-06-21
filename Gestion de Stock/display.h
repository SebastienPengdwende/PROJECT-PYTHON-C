#ifndef DISPLAY_H
#define DISPLAY_H

#include "product.h"


void set_color(int color);
void reset_color();

void display_product(const Prod *p);
void display_all_products(const Invent *inv);
void display_low_stock_products(const Invent *inv);
void display_inventory_statistics(const Invent *inv);
void search_product(const Invent *inv);
void display_recent_changes(int count);
void input_product(Prod *p);

#endif