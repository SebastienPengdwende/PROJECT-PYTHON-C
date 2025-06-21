#include <stdio.h>
#include <windows.h>
#include <time.h>
#include <string.h>
#include "display.h"

void set_color(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

void reset_color() {
    set_color(7);
}

void display_product(const Prod *p) {
    if (p->quantity == 0) {
        set_color(12);
    } else if (is_low_stock(p)) {
        set_color(14);
    } else {
        set_color(10);
    }

    printf("| %-20s | %-8s | %-12s | %4d | %14.2f FCFA | %10s |\n",
           p->name, p->id, p->category, p->quantity, p->price, p->date);

    reset_color();
}

void display_all_products(const Invent *inv) {
  printf("\n+----------------------+----------+--------------+------+---------------------+------------+\n");
    printf("| Name                 | ID       | Category     | Qty  | Price (FCFA)        | Date       |\n");
    printf("+----------------------+----------+--------------+------+---------------------+------------+\n");

    for (int i = 0; i < inv->product_count; i++) {
        display_product(&inv->products[i]);
    }

    printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
    printf("Total: %d product(s)\n", inv->product_count);
}

void display_low_stock_products(const Invent *inv) {
    printf("\n=== LOW STOCK PRODUCTS ===\n");
    int found = 0;

    for (int i = 0; i < inv->product_count; i++) {
        if (is_low_stock(&inv->products[i])) {
            if (!found) {
                printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
                printf("| Name                 | ID       | Category     | Qty  | Price (FCFA)        | Date       |\n");
                printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
            }
            display_product(&inv->products[i]);
            found = 1;
        }
    }

    if (!found) {
        printf("No products are currently low in stock.\n");
    } else {
        printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
    }
}

void display_inventory_statistics(const Invent *inv) {
    int total_qty = 0;
    float total_value = 0.0;
    int low_stock_count = 0;
    float average_price = 0.0;

    for (int i = 0; i < inv->product_count; i++) {
        total_qty += inv->products[i].quantity;
        total_value += inv->products[i].quantity * inv->products[i].price;
        if (is_low_stock(&inv->products[i])) {
            low_stock_count++;
        }
    }

    if (total_qty > 0) {
        average_price = total_value / total_qty;
    }

    printf("\n=== INVENTORY STATISTICS ===\n\n");

    printf("Total number of different products : %d\n", inv->product_count);
    printf("Total quantity of all products     : %d units\n", total_qty);
    printf("Total inventory value              : %.2f FCFA\n", total_value);
    printf("Average price per unit             : %.2f FCFA\n", average_price);
    printf("Products in low stock              : %d", low_stock_count);

    if (inv->product_count > 0) {
        float percent = (float)low_stock_count / inv->product_count * 100;
        printf(" (%.1f%%)\n", percent);
    } else {
        printf("\n");
    }

    if (low_stock_count > 0) {
                 printf("\nWarning: Some products are near or below the minimum threshold.\n");
                 printf("Tip    : Consider restocking these products to avoid running out.\n");

    } else {
        printf("\nTous les stocks sont suffisants actuellement.\n");
    }
}


void search_product(const Invent *inv) {
    char keyword[50];
    int found = 0;

    printf("\nEnter product name or ID to search: ");
    scanf("%s", keyword);

    printf("\n=== SEARCH RESULTS ===\n");

    for (int i = 0; i < inv->product_count; i++) {
        if (strstr(inv->products[i].name, keyword) != NULL ||
            strcmp(inv->products[i].id, keyword) == 0) {
            if (!found) {
                printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
                printf("| Name                 | ID       | Category     | Qty  | Price (FCFA)        | Date       |\n");
                printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
            }
            display_product(&inv->products[i]);
            found = 1;
        }
    }

    if (!found) {
        printf("No matching products found.\n");
    } else {
        printf("+----------------------+----------+--------------+------+---------------------+------------+\n");
    }
    getchar(); 
}

void display_recent_changes(int count) {
    FILE *f = fopen(LOG_FILE, "r");
    if (f == NULL) {
        printf("\nNo history available.\n");
        return;
    }

    char lines[100][256];
    int total = 0;

    while (fgets(lines[total], sizeof(lines[total]), f) && total < 100) {
        total++;
    }

    fclose(f);

    printf("\n=== RECENT CHANGES (Last %d) ===\n\n", count);
    int start = (total > count) ? total - count : 0;
    for (int i = start; i < total; i++) {
        printf("%s", lines[i]);
    }
}

void input_product(Prod *p) {
    printf("Name: ");
    scanf("%49s", p->name);

    printf("Category: ");
    scanf("%29s", p->category);

    printf("Quantity: ");
    scanf("%d", &p->quantity);

    printf("Price (FCFA): ");
    scanf("%f", &p->price);

    printf("Minimum stock before alert: ");
    scanf("%d", &p->min_stock);

    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    sprintf(p->date, "%04d-%02d-%02d", tm_info->tm_year + 1900, tm_info->tm_mon + 1, tm_info->tm_mday);
}
