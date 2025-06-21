#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include "product.h"
#include "file.h"
#include "display.h"
#include "modification.h"

void display_menu() {
    printf("\n");
    printf("+==============================================+\n");
    printf("|         INVENTORY MANAGEMENT SYSTEM          |\n");
    printf("+==============================================+\n");
    printf("| 1. Add a product                             |\n");
    printf("| 2. Modify a product                          |\n");
    printf("| 3. Delete a product                          |\n");
    printf("| 4. Display all products                      |\n");
    printf("| 5. Search for a product                      |\n");
    printf("| 6. View low stock products                   |\n");
    printf("| 7. Inventory statistics                      |\n");
    printf("| 8. View recent changes                       |\n");
    printf("| 9. Reset inventory and history               |\n");
    printf("| 0. Exit                                      |\n");
    printf("+==============================================+\n");
    printf("Your choice: ");
}

int main() {
    setlocale(LC_ALL, "");

    Invent inventory;
    init_invent(&inventory);
    load_inventory(&inventory);

    int choice;
    char id[10];
    Prod new_product;

    do {
        system("cls");
        display_menu();
        scanf("%d", &choice);
        getchar(); 

        switch (choice) {
            case 1:
                system("cls");
                printf("=== ADD PRODUCT ===\n\n");
                init_prod(&new_product);
                input_product(&new_product);
                generate_unique_id(new_product.id, &inventory);
                add_product(&inventory, new_product);
                break;

            case 2:
                system("cls");
                printf("Enter product ID to modify: ");
                scanf("%9s", id);
                modify_product(&inventory, id);
                break;

            case 3:
                system("cls");
                printf("Enter product ID to delete: ");
                scanf("%9s", id);
                delete_product(&inventory, id);
                break;

            case 4:
                system("cls");
                display_all_products(&inventory);
                break;

            case 5:
                system("cls");
                search_product(&inventory);
                break;

            case 6:
                system("cls");
                display_low_stock_products(&inventory);
                break;

            case 7:
                system("cls");
                display_inventory_statistics(&inventory);
                break;

            case 8:
                system("cls");
                display_recent_changes(10);
                break;

            case 9:
                system("cls");
                printf("Are you sure you want to reset inventory and history? (y/n): ");
                char confirm;
                scanf(" %c", &confirm);
                if (confirm == 'y' || confirm == 'Y') {
                    reset_inventory(&inventory);
                } else {
                    printf("\nReset cancelled.\n");
                }
                break;

            case 0:
                system("cls");
                printf("Goodbye!\n");
                break;

            default:
                system("cls");
                printf("Invalid choice. Try again.\n");
        }

        if (choice != 0) {
            printf("\nPress Enter to continue...");
            getchar();
        }

    } while (choice != 0);

    return 0;
}