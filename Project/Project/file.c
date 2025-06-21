#include <stdio.h>
#include <string.h>
#include "file.h"

int save_inventory(const Invent *inv) {
    FILE *f = fopen(Data, "w");
    if (f == NULL) {
        printf("Error: cannot save inventory.\n");
        return 0;
    }

    for (int i = 0; i < inv->product_count; i++) {
        Prod *p = &inv->products[i];
        fprintf(f, "%s,%s,%s,%d,%.2f,%d,%s\n",
                p->name, p->id, p->category,
                p->quantity, p->price, p->min_stock, p->date);
    }

    fclose(f);
    return 1;
}

int load_inventory(Invent *inv) {
    FILE *f = fopen(Data, "r");
    if (f == NULL) {
        return 0; 
    }

    inv->product_count = 0;
    char line[256];

    while (fgets(line, sizeof(line), f) && inv->product_count < Max) {
        Prod p;
        line[strcspn(line, "\n")] = '\0'; // retire le saut de ligne

        if (sscanf(line, "%49[^,],%9[^,],%29[^,],%d,%f,%d,%10[^,\n]",
                   p.name, p.id, p.category,
                   &p.quantity, &p.price, &p.min_stock, p.date) == 7) {
            inv->products[inv->product_count++] = p;
        }
    }

    fclose(f);
    return 1;
}
