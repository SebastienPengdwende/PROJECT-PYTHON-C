#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "modification.h"
#include "file.h"
#include "display.h"

int search_product_by_id(const Invent *inv, const char *id) {
    for (int i = 0; i < inv->product_count; i++) {
        if (strcmp(inv->products[i].id, id) == 0) {
            return i;
        }
    }
    return -1;
}

int add_product(Invent *inv, Prod p) {
    if (inv->product_count >= Max) {
        system("cls");
        printf("\nError: Inventory is full.\n");
        return 0;
    }

    if (search_product_by_id(inv, p.id) != -1) {
        system("cls");
        printf("\nError: A product with this ID already exists.\n");
        return 0;
    }

    inv->products[inv->product_count++] = p;

    log_inventory_change(ADD_PRODUCT, NULL, &p);
    save_inventory(inv);

    system("cls");
    printf("\nProduct added successfully!\n");
    return 1;
}

int modify_product(Invent *inv, const char *id) {
    int index = search_product_by_id(inv, id);
    if (index == -1) {
        system("cls");
        printf("\nError: Product not found.\n");
        return 0;
    }

    Prod original = inv->products[index];
    system("cls");
    printf("\nModifying product '%s'\n\n", original.name);

    printf("+----------------------+----------+--------------+------+----------------------+------------+\n");
    printf("| Name                 | ID       | Category     | Qty  | Price (FCFA)         | Date       |\n");
    printf("+----------------------+----------+--------------+------+----------------------+------------+\n");
    display_product(&original);
    printf("+----------------------+----------+--------------+------+----------------------+------------+\n\n");

    printf("New name (%s): ", original.name);
    char buffer[50];
    scanf("%49s", buffer);
    if (strlen(buffer) > 0) strcpy(inv->products[index].name, buffer);

    printf("New category (%s): ", original.category);
    scanf("%29s", buffer);
    if (strlen(buffer) > 0) strcpy(inv->products[index].category, buffer);

    printf("New quantity (%d): ", original.quantity);
    int qty;
    scanf("%d", &qty);
    if (qty >= 0) inv->products[index].quantity = qty;

    printf("New price (%.2f FCFA): ", original.price);
    float price;
    scanf("%f", &price);
    if (price >= 0) inv->products[index].price = price;

    printf("New min stock (%d): ", original.min_stock);
    int threshold;
    scanf("%d", &threshold);
    if (threshold >= 0) inv->products[index].min_stock = threshold;

    log_inventory_change(MODIFY_PRODUCT, &original, &inv->products[index]);
    save_inventory(inv);

    system("cls");
    printf("\nProduct modified successfully!\n");
    return 1;
}

int delete_product(Invent *inv, const char *id) {
    int index = search_product_by_id(inv, id);
    if (index == -1) {
        system("cls");
        printf("\nError: Product not found.\n");
        return 0;
    }

    Prod deleted = inv->products[index];

    system("cls");
    printf("\nDeleting the following product:\n\n");
    printf("+----------------------+----------+--------------+------+----------------------+------------+\n");
    printf("| Name                 | ID       | Category     | Qty  | Price (FCFA)         | Date       |\n");
    printf("+----------------------+----------+--------------+------+----------------------+------------+\n");
    display_product(&deleted);
    printf("+----------------------+----------+--------------+------+----------------------+------------+\n");

    printf("\nAre you sure you want to delete this product? (y/n): ");
    char confirm;
    scanf(" %c", &confirm);
    if (confirm != 'y' && confirm != 'Y') {
        printf("Deletion cancelled.\n");
        return 0;
    }

    for (int i = index; i < inv->product_count - 1; i++) {
        inv->products[i] = inv->products[i + 1];
    }
    inv->product_count--;

    log_inventory_change(DELETE_PRODUCT, &deleted, NULL);
    save_inventory(inv);

    system("cls");
    printf("\nProduct deleted successfully!\n");
    return 1;
}

void log_inventory_change(Change change, const Prod *before, const Prod *after) {
    FILE *log = fopen(LOG_FILE, "a");
    if (log == NULL) return;

    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char timestamp[20];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", t);

    const char *action = (change == ADD_PRODUCT) ? "ADDED" :
                         (change == MODIFY_PRODUCT) ? "MODIFIED" : "DELETED";

    if (change == ADD_PRODUCT && after) {
        fprintf(log, "[%s] %s: %s (ID: %s, Qty: %d, Price: %.2f)\n",
                timestamp, action, after->name, after->id, after->quantity, after->price);
    } else if (change == DELETE_PRODUCT && before) {
        fprintf(log, "[%s] %s: %s (ID: %s, Qty: %d, Price: %.2f)\n",
                timestamp, action, before->name, before->id, before->quantity, before->price);
    } else if (change == MODIFY_PRODUCT && before && after) {
        fprintf(log, "[%s] %s: %s (ID: %s)\n", timestamp, action, after->name, after->id);
    }

    fclose(log);
}

void reset_inventory(Invent *inv) {
    inv->product_count = 0;

    FILE *f = fopen(Data, "w");
    if (f) fclose(f);

    FILE *log = fopen(LOG_FILE, "w");
    if (log) fclose(log);

    system("cls");
    printf("\n? Inventory and history have been reset successfully.\n");
}