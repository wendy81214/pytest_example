PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE cm_cust_product_code(
customer_id varchar not null primary key,
product_code varchar);
INSERT INTO cm_cust_product_code VALUES('1','BNDF');
INSERT INTO cm_cust_product_code VALUES('2','ETFF');
INSERT INTO cm_cust_product_code VALUES('3','STKF');
COMMIT;
