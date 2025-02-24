/*
  Warnings:

  - You are about to drop the column `purchases` on the `User` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "purchases",
ALTER COLUMN "password" DROP DEFAULT;
