#ifndef MODIFICATION_H
#define MODIFICATION_H

#include "product.h"

int add_product(Invent *inv, Prod p);
int modify_product(Invent *inv, const char *id);
int delete_product(Invent *inv, const char *id);
int search_product_by_id(const Invent *inv, const char *id);
void log_inventory_change(Change change, const Prod *before, const Prod *after);
void reset_inventory(Invent *inv);  

#endif
