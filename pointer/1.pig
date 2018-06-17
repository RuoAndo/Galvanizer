C = LOAD '$COUNT' USING PigStorage(',') AS (fn:chararray, item1:int, item2:int, item3:int, item4:int);
dump C;

-- *height,62,radix_tree_extend:xen/common/radix-tree.c:55

P = LOAD '$POINT' USING PigStorage(',') AS (pname:chararray, line1:int, path:chararray, line2:int);
dump P;