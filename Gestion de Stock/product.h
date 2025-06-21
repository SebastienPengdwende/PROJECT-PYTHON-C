#ifndef PRODUCT_H
#define PRODUCT_H

#define Max 1000
#define Data "data.txt"
#define LOG_FILE "inventory.txt"

typedef struct {
    char name[50];
    char id[10];
    char category[30];
    int quantity;
    float price;
    char date[11];
    int min_stock;
} Prod;

typedef struct {
    Prod products[Max];
    int product_count;
} Invent;

typedef enum {
    ADD_PRODUCT,
    MODIFY_PRODUCT,
    DELETE_PRODUCT
} Change;

void init_prod(Prod *p);
void init_invent(Invent *inv);
int is_low_stock(const Prod *p);
int count_low_stock_products(const Invent *inv);
void generate_unique_id(char *id, const Invent *inv);
#endif