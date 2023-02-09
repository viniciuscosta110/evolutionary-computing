#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 8

int board[MAX][MAX];
int count = 0;

void printBoard()
{
    for (int i = 0; i < MAX; i++)
    {
        for (int j = 0; j < MAX; j++)
        {
            printf("%d ", board[i][j]);
        }

        printf("\n");
    }

    printf("\n");
}

// check if the position is valid
int check(int row, int col)
{
    // check row
    for (int i = 0; i < col; i++)
        if (board[row][i] == 1)
            return 0;

    // check diagonals
    for(int i = 0; i < MAX; i++)
    {
        for(int j = 0; j < MAX; j++)
        {
            if(board[i][j] == 1 && j != col && i != row)
            {
                int x = abs(i - row);
                int y = abs(j - col);

                if(x == y) return 0;
            }
        }
    }
    
    return 1;
}

void solve(int col)
{
    if (col == MAX)
    {
        printBoard();
        count++;
        return;
    }

    for (int i = 0; i < MAX; i++)
    {
        //Check if the position is valid
        if(check(i, col))
        {
            // place the queen
            board[i][col] = 1;

            // solve for the next column
            solve(col + 1);

            // backtrack
            board[i][col] = 0;
        }
    }
}

int main(int argc, char *argv[])
{
    // Initialize the board
    for (int i = 0; i < MAX; i++)
        for (int j = 0; j < MAX; j++)
            board[i][j] = 0;

    solve(0);
    printf("Total solutions: %d", count);

    return 0;
}