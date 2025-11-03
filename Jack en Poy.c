#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char player1, player2;
    int player1_score = 0, player2_score = 0;
    char choice;
    char inputBuffer[256];

    do {
        system("cls");

        printf("*===========================================*\n");
        printf("*                                           *\n");
        printf("*          Welcome to Rock Paper Scissors   *\n");
        printf("*                                           *\n");
        printf("*===========================================*\n\n");
        printf("*===========================================*\n");
        printf("*              P for paper                  *\n");
        printf("*              R for rock                   *\n");
        printf("*              S for scissors               *\n");
        printf("*===========================================*\n\n");

        printf("Player 1: Enter your choice (R for Rock, P for Paper, S for Scissors): ");
        while (1) {
            if (scanf(" %c", &player1) != 1 || (player1 != 'R' && player1 != 'r' && player1 != 'P' && player1 != 'p' && player1 != 'S' && player1 != 's')) {
                printf("\nInvalid input. Please enter R, P, or S.\n");
                printf("Choose R, P, S: ");
                while (getchar() != '\n');
            } else if (getchar() != '\n') {
                printf("\nInvalid input. Please enter only one character.\n");
                printf("Choose R, P, S: ");
                while (getchar() != '\n');
            } else {
                break;
            }
        }

        printf("\nPlayer 2: Enter your choice (R for Rock, P for Paper, S for Scissors): ");
        while (1) {
            if (scanf(" %c", &player2) != 1 || (player2 != 'R' && player2 != 'r' && player2 != 'P' && player2 != 'p' && player2 != 'S' && player2 != 's')) {
                printf("\nInvalid input. Please enter R, P, or S.\n");
                printf("Choose R, P, S: ");
                while (getchar() != '\n');
            } else if (getchar() != '\n') {
                printf("\nInvalid input. Please enter only one character.\n");
                printf("Choose R, P, S: ");
                while (getchar() != '\n');
            } else {
                break;
            }
        }

        if ((player1 == 'R' || player1 == 'r') && (player2 == 'S' || player2 == 's') ||
            (player1 == 'P' || player1 == 'p') && (player2 == 'R' || player2 == 'r') ||
            (player1 == 'S' || player1 == 's') && (player2 == 'P' || player2 == 'p')) {
            printf("\nPlayer 1 wins!\n");
            player1_score++;
        } else if ((player2 == 'R' || player2 == 'r') && (player1 == 'S' || player1 == 's') ||
                   (player2 == 'P' || player2 == 'p') && (player1 == 'R' || player1 == 'r') ||
                   (player2 == 'S' || player2 == 's') && (player1 == 'P' || player1 == 'p')) {
            printf("\nPlayer 2 wins!\n");
            player2_score++;
        } else {
            printf("\nIt's a tie!\n");
        }
        printf("\n*================*\n");
        printf("Player 1 Score: %d\n", player1_score);
        printf("Player 2 Score: %d\n", player2_score);
        printf("*================*\n");
        do {
            printf("\nDo you want to play again? (Y/N): ");
            scanf(" %c", &choice);
            if (choice != 'Y' && choice != 'N' && choice != 'y' && choice != 'n') {
                printf("\nInvalid input. Please enter Y or N.\n");
                while (getchar() != '\n');
            }
        } while (choice != 'Y' && choice != 'N' && choice != 'y' && choice != 'n');

    } while (choice == 'Y' || choice == 'y');

    if (choice == 'N' || choice == 'n') {
        system("cls");
        printf("*===========================*\n");
        printf("*  Thank you for playing!!! *\n");
        printf("*===========================*");
    }

    return 0;
}
