syntax='
BEGIN;
--
-- Create model ProductBooking
--
CREATE TABLE "sales_productbooking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking" integer NOT NULL, "returns" integer NOT NULL);
--
-- Create model VendorBooking
--
CREATE TABLE "sales_vendorbooking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "closed" bool NOT NULL, "paid" bool NOT NULL, "total" real NULL, "amount_paid" real NULL, "vendor_id" integer NOT NULL REFERENCES "agent_vendor" ("id"));
--
-- Add field master_booking to productbooking
--
ALTER TABLE "sales_productbooking" RENAME TO "sales_productbooking__old";
CREATE TABLE "sales_productbooking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking" integer NOT NULL, "returns" integer NOT NULL, "master_booking_id" integer NOT NULL REFERENCES "sales_vendorbooking" ("id"));
INSERT INTO "sales_productbooking" ("returns", "id", "booking", "master_booking_id") SELECT "returns", "id", "booking", NULL FROM "sales_productbooking__old";
DROP TABLE "sales_productbooking__old";
CREATE INDEX "sales_vendorbooking_96b1f972" ON "sales_vendorbooking" ("vendor_id");
CREATE INDEX "sales_productbooking_f3fec6c1" ON "sales_productbooking" ("master_booking_id");
--
-- Add field product to productbooking
--
ALTER TABLE "sales_productbooking" RENAME TO "sales_productbooking__old";
CREATE TABLE "sales_productbooking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking" integer NOT NULL, "returns" integer NOT NULL, "master_booking_id" integer NOT NULL REFERENCES "sales_vendorbooking" ("id"), "product_id" integer NOT NULL REFERENCES "utils_product" ("id"));
INSERT INTO "sales_productbooking" ("returns", "product_id", "id", "booking", "master_booking_id") SELECT "returns", NULL, "id", "booking", "master_booking_id" FROM "sales_productbooking__old";
DROP TABLE "sales_productbooking__old";
CREATE INDEX "sales_productbooking_f3fec6c1" ON "sales_productbooking" ("master_booking_id");
CREATE INDEX "sales_productbooking_9bea82de" ON "sales_productbooking" ("product_id");
COMMIT;'
