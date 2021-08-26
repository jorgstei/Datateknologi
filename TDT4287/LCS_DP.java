import java.util.Scanner;

class LCS_DP{

    public static void main(String[] args){
        
        LCS_DP lcs = new LCS_DP();
        /*
        //In case of user input
        Scanner sc = new Scanner(System.in);
        System.out.println("String 1:");
        String str1 = sc.nextLine();
        System.out.println("String 2:");
        String str2 = sc.nextLine();
        System.out.println("Strings are: '" + str1 + "' and '" + str2 + "'");
        */
        // Problem 1: LCS(ATTCGGTTA, TAGTGATG) - TTGT
        String str1 = "ATTCGGTTA";
        String str2 = "TAGTGATG";
        int[][] matrix = new int[str1.length()+1][str2.length()+1];

        // The 2d array is already initialized to all zeros, but why not
        for (int i = 0; i < matrix.length; i++) {
            matrix[i][0] = 0;
        }
        for (int i = 0; i < matrix[0].length; i++) {
            matrix[0][i] = 0;
        }
        System.out.println("Initialized:\n" + lcs.matrixToString(str2, str1, matrix));

        // i is row, j is column
        for (int i = 1; i < matrix.length; i++) {
            for (int j = 1; j < matrix[0].length; j++) {
                if(str1.charAt(i-1) == str2.charAt(j-1)){
                    matrix[i][j] = lcs.max(matrix[i-1][j-1] + 1, matrix[i-1][j], matrix[i][j-1]);
                }
                else{
                    matrix[i][j] = lcs.max(matrix[i-1][j], matrix[i][j-1], -1);
                }
            }
        }
        System.out.println("Solved:\n" + lcs.matrixToString(str2, str1, matrix));
        
        System.out.println("LCS is " + lcs.getLCS(str1, str2, matrix));

    }

    public int max(int int1, int int2){
        if(int1 >= int2 ){
            return int1;
        }
        else{
            return int2;
        }
    }

    public int max(int int1, int int2, int int3){
        if(int1 >= int2 && int1 >= int3){
            return int1;
        }
        else if(int2 >= int1 && int2 >= int3){
            return int2;
        }
        else{
            return int3;
        }
    }
    // Get the LCS without using a backtrack matrix
    public String getLCS(String str1, String str2, int[][] solvedMatrix){
        String lcs = "";
        int currentY = solvedMatrix.length - 1;
        int currentX = solvedMatrix[0].length - 1;
        while(lcs.length() < solvedMatrix[solvedMatrix.length-1][solvedMatrix[0].length-1]){
            // If diagonal (left/up) is smaller than current
            if(solvedMatrix[currentY][currentX] > solvedMatrix[currentY-1][currentX-1]){
                lcs = str1.charAt(currentY) + lcs;
                currentX -= 1;
                currentY -= 1;
            }
            // If left is smaller than current (not sure if this ever happens tbh)
            else if(solvedMatrix[currentY][currentX] > solvedMatrix[currentY][currentX-1]){
                lcs = str1.charAt(currentY) + lcs;
                currentX -= 1;
            }
            // If above is smaller than current (not sure if this one happens either)
            else if(solvedMatrix[currentY][currentX] > solvedMatrix[currentY-1][currentX]){
                lcs = str1.charAt(currentY) + lcs;
                currentY-= 1;
            }
            else{
                currentY-=1;
            }
        }
        return lcs;
    }
    public String[] getEveryLCS(String str1, String str2, int[][] solvedMatrix){
        String[] everyLCS = {"who", "knows"};
        return everyLCS;
    }

    public String matrixToString(String cols, String rows, int[][] matrix){
        String res = "x ε ";
        for (int i = 0; i < cols.length(); i++) {
            res += cols.charAt(i) + " ";
        }
        res += "\n";
        for (int i = 0; i < matrix.length; i++) {
            if(i==0){res+="ε ";}
            else{res+=rows.charAt(i-1)+" ";}
            for (int j = 0; j < matrix[0].length; j++) {
                res += matrix[i][j] + " ";
            }
            res += "\n";
        }
        return res;
    }
}

