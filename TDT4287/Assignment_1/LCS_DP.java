package Assignment_1;

import java.util.*;
import java.util.stream.Collectors;

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
        // Problem 1: LCS(ATTCGGTTA, TAGTGATG) = TTGT, ATGT, TGTA
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

        // i is rows, j is columns
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

        List<String> listWithoutDuplicates = lcs.getEveryLCS(str1, str2, matrix.length - 1, matrix[0].length - 1, matrix).stream().distinct().collect(Collectors.toList());
        System.out.println("Every LCS is: " + listWithoutDuplicates.toString());

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
    // Get the LCS without using a backtracking matrix
    // This sorta uses the same concept as a backtracking matrix, just without the matrix, not sure if you were looking for a different solution.
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
                currentY -= 1;
            }
            else{
                currentY -= 1;
            }
        }
        return lcs;
    }
    // Heavily inspired by https://www.techiedelight.com/longest-common-subsequence-finding-lcs/
    public ArrayList<String> getEveryLCS(String str1, String str2, int currY, int currX, int[][] solvedMatrix){
        // If we reach the end of either str
        if(currY == 0 || currX == 0){
            ArrayList<String> emptyArr = new ArrayList<String>();
            emptyArr.add("");
            return emptyArr;
        }

        // If the last character of strs match
        if(str1.charAt(currY-1) == str2.charAt(currX-1)){
            ArrayList<String> lcs = getEveryLCS(str1, str2, currY-1, currX-1, solvedMatrix);
            // Add the matching character to every subsequence
            for (int i = 0; i < lcs.size(); i++) {
                lcs.set(i, lcs.get(i) + str1.charAt(currY-1));
            }
            return lcs;
        }

        else{
            // If above is higher than left
            if(solvedMatrix[currY-1][currX] > solvedMatrix[currY][currX-1]){
                return getEveryLCS(str1, str2, currY-1, currX, solvedMatrix);
            }
            // If left is higher than above
            else if(solvedMatrix[currY][currX-1] > solvedMatrix[currY-1][currX]){
                return getEveryLCS(str1, str2, currY, currX-1, solvedMatrix);
            }
            // If left and above are equal
            else{
                ArrayList<String> above = getEveryLCS(str1, str2, currY-1, currX, solvedMatrix);
                ArrayList<String> left = getEveryLCS(str1, str2, currY, currX-1, solvedMatrix);
            
                above.addAll(left);
                
                return above;
            }
        }
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

